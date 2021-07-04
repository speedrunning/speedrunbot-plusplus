#!/usr/bin/env sh

die () {
	>&2 echo "$1"
	exit 1
}

download () (
	2>/dev/null curl "https://www.speedrun.com/$1/allposts/[$2-$(( $2 + REQS_PER_CORE - 1 ))]" |
		sed -En "s|\s+<p class=\"mb-1\">Forum: <a href='/([^/]+)/forum'>.*</a></p>|\1|p" >>/tmp/$3
)

[ $1 ] || die 'Usage: `+posts [PLAYER NAME]`
Example: `+posts AnInternetTroll`'

set -e

# In the sed(1) command we branch to `:quit` the moment we match, if not it will match twice.
MAX=$(2>/dev/null curl "https://www.speedrun.com/$1/allposts" | sed -En '
b sub
:quit
q
:sub
s|\s+<li class="page-item"><a class="page-link page-info">Page 1 of ([0-9]+)</a></li>|\1|p
t quit')

# TODO: Add better error messages maybe?
[ -z $MAX ] && die "User '$1' is either not real, or has no posts. (Or the site is down)"

REQS_PER_CORE=$(( MAX / 4 ))

trap "rm -f /tmp/$$" EXIT

i=1
until [ $i -gt $MAX ]; do
	for _ in 1 2 3 4; do
		download "$1" $i $$ &
		: $(( i += REQS_PER_CORE ))
	done
	wait
done

while read LINE; do
	case $LINE in
	introductions|speedrunning|streaming_recording_equipment|tournaments_and_races|talk|the_site)
		: $(( SITE += 1 ))
		;;
	*)
		: $(( GAME += 1 ))
		;;
	esac
done </tmp/$$

TOTAL=$(2>/dev/null curl "https://www.speedrun.com/user/$1/info" |
	sed -En 's/.*Posts:[^[:digit:]]+([0-9]+).*/\1/p')

echo "Site Forums: $SITE
Game Forums: $GAME
Secret Forums: $(( TOTAL - SITE - GAME ))
Total: $TOTAL"
