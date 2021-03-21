#!/usr/bin/env sh

# This is the setup script for the bot.

install_python39() {
	$SU apt update
	yes | $SU apt install build-essential zlib1g-dev libncurses5-dev \
		libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev \
		libreadline-dev libffi-dev curl libbz2-dev

	wget https://www.python.org/ftp/python/3.9.1/Python-3.9.1.tgz
	tar -xf Python-3.9.1.tgz

	cd Python-3.9.1 || exit 1
	./configure --enable-optimizations
	make -j "$(nproc)"
	$SU make altinstall

	cd ../
	$SU rm -rf Python-3.9.1 Python-3.9.1.tgz
}

SCR_PATH=$(cd "$(dirname "$0")" && pwd)

# I'm very cool and use Doas instead of Sudo. Doas gang rise up.
printf "Command to gain superuser privileges [sudo]: "
read -r SU
test "$SU" = "" && SU="sudo"

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
if ! command -v python3 >/dev/null 2>&1; then
	echo "You must install python3 before setting up the bot. Python 3.9 is recommended."
	exit 0
elif ! command -v python3.9 >/dev/null 2>&1; then
	echo "WARNING: Python3.9 is not installed. There is no guarantee the bot will work."
	printf "Do you want to install python3.9? (Only tested on Debian) [y/N]: "
	read -r C

	if test "$C" = "y" || test "$C" = "Y"; then
		install_python39
	fi
fi

# Install dependencies
echo "Installing dependencies..."
if command -v python3.9 >/dev/null 2>&1; then
	PY="python3.9"
else
	PY="python3"
fi
$PY -m pip install -r requirements.txt >/dev/null 2>&1

# Assuming debian based, everyone else needs to deal with it.
yes | $SU apt install libjansson-dev libcurl4-openssl-dev >/dev/null 2>&1

# Run the Makefiles.
cd "$SCR_PATH"/src/srcom && make CCMP=$CC
