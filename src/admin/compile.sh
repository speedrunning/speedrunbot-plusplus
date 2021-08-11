#!/usr/bin/env sh

[ "$1" = "clean" ] && CLEAN=true || CLEAN=false

cd "${0%/*}"
for MAKEFILE in $(find ../../ -name 'Makefile'); do
	( cd "${MAKEFILE%/*}"
	$CLEAN && { make clean; make; } || make )
done
