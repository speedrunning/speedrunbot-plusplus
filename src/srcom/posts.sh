#!/usr/bin/env sh

NOT_REAL="User with name '%s' not found.\n"
USAGE='Usage: `+posts [-v|--verbose] [PLAYER NAME]`
Example: `+posts AnInternetTroll`'

die () {
	>&2 echo "$1"
	exit 1
}

download () (
	2>/dev/null curl "https://www.speedrun.com/$1/allposts/[$2-$(( $2 + REQS_PER_CORE - 1 ))]" |
		sed -En "s|\s+<p class=\"mb-1\">Forum: <a href='/([^/]+)/forum'>.*</a></p>|\1|p" >>/tmp/$3
)

verbose () {
	set -e

	MAX=$(2>/dev/null curl "https://www.speedrun.com/$1/allposts" | sed -En '
# Just in case
0,/<div class="widget-title">Forum posts<\/div>/d

# Get the number of pages
/Page 1 of [0-9]+/ {
	s|\s+<li class="page-item"><a class="page-link page-info">Page 1 of ([0-9]+)</a></li>|\1|p
	q
}')

	[ $MAX -eq 0 ] && {
		echo 'Site Forums: 0
Game Forums: 0
Secret Forums: 0
Total: 0'
		exit 1
	}

	REQS_PER_CORE=$(( MAX / 4 ))

	trap 'rm -f /tmp/$$' EXIT

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

	echo "Site Forums: $SITE
Game Forums: $GAME
Secret Forums: $(( TOTAL - SITE - GAME ))
Total: $TOTAL"
}

# Because of the fact that getting the more verbose data is so much slower, we require the user to
# supply a flag to actually enable it.
case "$1" in
-v|--verbose)
	VERBOSE=1
	shift
	;;
esac

# Check that the right amount of arguements have been specified.
[ $# -ne 1 ] && die "$USAGE"

# Crash on error.
set -e

# Get the number of posts that the user has.
TOTAL=$(2>/dev/null curl "https://www.speedrun.com/user/$1/info" | sed -n '
/User [a-zA-Z0-9_]* not found\./q

# Just in case
0,/<div>Info<\/div>/d

# Get the number of total posts.
/Posts:/ {
	s/.*Posts:[^0-9]*\([0-9]*\).*/\1/p
	# We have all the required data, so we can quit.
	q
}
')

# Error out if the user is not real, otherwise check if the verbose flag was specified and act
# accordingly.
[ -z $TOTAL ] && {
	>&2 printf "$NOT_REAL" "$1"
	exit 1
}
[ $VERBOSE ] && verbose "$1" || echo "Forum Posts: $TOTAL"
