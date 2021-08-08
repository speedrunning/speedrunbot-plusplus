#!/usr/bin/env sh

# This is the setup script for the bot.

install_python39() {
	$SU apt update
	yes | $SU apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev
		libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev

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
if command -v doas >/dev/null 2>&1; then
	SU="doas"
elif command -v sudo >/dev/null 2>&1; then
	SU="sudo"
else
	printf "Command to gain superuser privileges (typically sudo or doas): "
	read -r SU
fi

# Check for C compilers.
echo Checking for C compiler
if ! command -v cc gcc clang >/dev/null 2>&1; then
	echo You must install a C compiler before setting up the bot. If the installed compiler is \
		not GCC or Clang, make sure to link it to /bin/cc.
	exit 1
fi

# Check for Python 3.9.
echo Checking for Python3.9
if command -v python3.9 >/dev/null 2>&1; then
	PY="python3.9"
elif command -v python3 >/dev/null 2>&1; then
	echo WARNING: Python3 was found but not Python3.9. There is no guarantee the bot will work.
	printf "Do you want to install python3.9? (Only tested on Debian) [y/N]: "

	read -r C
	if test "$C" = "y" || test "$C" = "Y"; then
		PY="python3.9"
		install_python39
	else
		PY="python3"
	fi
else
	echo ERROR: Python3 was not found. The bot will not work. You can either install Python3 \
		from your distributions package manager or you can install Python3.9 from this \
		script.
	printf "Do you want to install python3.9? (Only tested on Debian) [y/N]: "

	read -r C
	if test "$C" = "y" || test "$C" = "Y"; then
		PY="python3.9"
		install_python39
	else
		exit 1
	fi
fi

# Check for OS via the package manager
if command -v apt >/dev/null 2>&1; then
	OS="debian"
elif command -v pacman >/dev/null 2>&1; then
	OS="arch"
fi

# Install dependencies
echo Installing dependencies
$PY -m pip install -r requirements.txt

case $OS in
arch)
	yes | $SU pacman -S curl jansson redis
	;;
debian)
	yes | $SU add-apt-repository ppa:redislabs/redis
	yes | $SU apt update
	yes | $SU apt install libjansson-dev libcurl4-openssl-dev redis
	;;
*)
	echo You do not have a supported OS. Please install libjansson, libcurl and redis manually
	exit 1
	;;
esac

$SU systemctl start redis

printf "Do you want to start redis on startup? [y/N]: "

read -r C

if test "$C" = "y" || test "$C" = "Y"; then
	$SU systemctl enable redis
fi


# Run the Makefiles.
cd "$SCR_PATH/src/admin"
make
./bin/compile
