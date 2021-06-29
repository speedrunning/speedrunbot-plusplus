#!/usr/bin/env sh

die () {
	echo "$1" >&2
	exit 1
}

[ $1 ] || die 'Usage: `+posts [PLAYER NAME]`
Example: `+posts AnInternetTroll`'

POSTS=$(curl "https://www.speedrun.com/user/$1/info" 2>/dev/null |
	sed -En 's/.*Posts:[^[:digit:]]*([0-9]+).*/\1/p')

[ $POSTS ] && echo $POSTS || die 'Either an incorrect username, or the site is down'
