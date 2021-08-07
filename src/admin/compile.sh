#!/usr/bin/env sh

cd "${0%/*}"
for MAKEFILE in $(find ../../ -name 'Makefile'); do
	( cd "${MAKEFILE%/*}" && make )
done
