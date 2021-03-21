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
echo Checking for program to grant superuser privileges
if command -v sudo >/dev/null 2>&1; then
	SU="sudo"
elif command -v doas >/dev/null 2>&1; then
	SU="doas"
else
	printf "Command to gain superuser privileges (typically sudo or doas): "
	read -r SU
fi

# Check for C compilers. Clang is preferred, then GCC, then the systems default.
echo Checking for C compiler
if command -v clang >/dev/null 2>&1; then
	CC="clang"
elif command -v gcc >/dev/null 2>&1; then
	CC="gcc"
elif command -v cc >/dev/null 2>&1; then
	CC="cc"
else
	echo You must install a C compiler before setting up the bot. Clang or \
		GCC are recommended.
	exit 0
fi

# Check for Python 3.9.
echo Checking for Python3.9
if command -v python3.9 >/dev/null 2>&1; then
	PY="python3.9"
elif command -v python3 >/dev/null 2>&1; then
	echo WARNING: Python3 was found but not Python3.9. There is no \
		guarantee the bot will work.
	install_python39
	printf "Do you want to install python3.9? (Only tested on Debian) [y/N]: "
	read -r C

	if test "$C" = "y" || test "$C" = "Y"; then
		PY="python3.9"
		install_python39
	else
		PY="python3"
	fi
else
	echo ERROR: Python3 was not found. The bot will not work. You can \
		either install Python3 from your distributions package manager \
		or you can install Python3.9 from this script.
	printf "Do you want to install python3.9? (Only tested on Debian) [y/N]: "
	read -r C

	if test "$C" = "y" || test "$C" = "Y"; then
		PY="python3.9"
		install_python39
	else
		exit 1
	fi
fi

# Install dependencies
echo Installing dependencies
$PY -m pip install -r requirements.txt >/dev/null 2>&1

# Assuming debian based, everyone else needs to deal with it.
yes | $SU apt install libjansson-dev libcurl4-openssl-dev >/dev/null 2>&1

# Run the Makefiles.
echo Building executables
cd "$SCR_PATH"/src/srcom && make CCMP=$CC >/dev/null 2>&1
