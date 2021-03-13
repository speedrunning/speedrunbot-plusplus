#!/usr/bin/env sh

# This is the setup script for the bot.

# Check for C compilers. Clang is preferred, then GCC, then the systems default.
if command -v clang >/dev/null 2>&1; then
	CC="clang"
elif command -v gcc >/dev/null 2>&1; then
	CC="gcc"
elif command -v cc >/dev/null 2>&1; then
	CC="cc"
else
	echo "You must install a C compiler before setting up the bot. Clang or GCC are recommended."
	exit 0
fi

# Check for Python 3.9.
if ! command -v python >/dev/null 2>&1; then
	echo "You must install python before setting up the bot. Python 3.9 is recommended."
	exit 0
elif ! command -v python3.9 >/dev/null 2>&1; then
	echo "WARNING: Python3.9 is not installed. There is no guarantee the bot will work."
fi

# Run the Makefiles.
SCR_PATH=$(cd "$(dirname "$0")" && pwd)
cd "$SCR_PATH"/src/srcom && make CC=$CC
