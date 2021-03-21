#!/usr/bin/env bash

# Format all the source files.

if ! command -v black &>/dev/null; then
	echo Error: Black was not found. This script will break when \
		formatting python files.
	printf "Do you want to install black? [y/N]: "
	read -r C
	if test "$C" = "y" || test "$C" = "Y"; then
		python3 -m pip install black
	fi
fi
if ! command -v isort &>/dev/null; then
	echo Error: isort was not found. This script will break when \
		formatting python files.
	printf "Do you want to install isort? [y/N]: "
	read -r C
	if test "$C" = "y" || test "$C" = "Y"; then
		python3 -m pip install isort
	fi
fi
if ! command -v clang-format &>/dev/null; then
	echo Error: clang-format was not found. This script will break when \
		formatting C files.
	printf "Do you want to install clang-format? (Debian only) [y/N]: "
	read -r C
	if test "$C" = "y" || test "$C" = "Y"; then
		if command -v sudo >/dev/null 2>&1; then
			SU="sudo"
		elif command -v doas >/dev/null 2>&1; then
			SU="doas"
		else
			printf "Command to gain superuser privileges (typically sudo or doas): "
			read -r SU
		fi
		yes | $SU apt install clang-format
	fi
fi

shopt -s globstar nullglob

SCR_PATH=$(cd "$(dirname "$0")" && pwd)

for FILE in "$SCR_PATH"/**/*; do
	case $FILE in
	*.[ch])
		clang-format -i --verbose --sort-includes -style=file "$FILE"
		;;
	*.py)
		echo Formatting "$FILE"
		isort "$FILE" &>/dev/null
		python3.9 -m black -l 80 "$FILE" &>/dev/null
		unexpand -t 4 --first-only "$FILE" >temp
		if test -x "$FILE"; then
			EFLAG=1
		else
			EFLAG=0
		fi
		mv temp "$FILE"
		test $EFLAG -eq 1 && chmod +x "$FILE"
		;;
	*.sh)
		echo Formatting "$FILE"
		unexpand -t 8 --first-only "$FILE" >temp
		mv temp "$FILE"
		chmod +x "$FILE"
		;;
	esac
done
