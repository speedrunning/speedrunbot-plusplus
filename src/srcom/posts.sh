#!/usr/bin/env sh

die () {
	echo "$1" >&2
	exit 1
}

download () (
	curl "https://www.speedrun.com/$1/allposts/$2" 2>/dev/null |
		sed -En "s|\s+<p class=\"mb-1\">Forum: <a href='/([^/]+)/forum'>.*</a></p>|\1|p" >>/tmp/$3
)

[ $1 ] || die 'Usage: `+posts [PLAYER NAME]`
Example: `+posts AnInternetTroll`'

# In the sed(1) command we branch to `:quit` the moment we match, if not it will match twice.
MAX=$(curl "https://www.speedrun.com/$1/allposts" 2>/dev/null | sed -En '
b sub
:quit
q
:sub
s|\s+<li class="page-item"><a class="page-link page-info">Page 1 of ([0-9]+)</a></li>|\1|p
t quit')

# TODO: Add better error messages maybe?
[ -z $MAX ] && die "User '$1' is either not real, or has no posts. (Or the site is down)"

trap "rm -f /tmp/$$" EXIT

i=0
until [ $i -gt $MAX ]; do
	for _ in 1 2 3 4; do
		: $(( i += 1 ))
		download "$1" $i $$ &
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

echo "Site Forums: $SITE
Game Forums: $GAME
Total: $(( SITE + GAME ))"
