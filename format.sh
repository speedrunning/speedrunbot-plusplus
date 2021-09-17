#!/usr/bin/env bash

# Format all the source files.

prompt_user() {
	echo Error: $1 was not found. This script will break when formatting $2 files.
	printf "Do you want to install $1? [y/N]: "
	read -r C
	if test "$C" = "y" || test "$C" = "Y"; then
		return 0
	fi
	return 1
}

if ! command -v black >/dev/null; then
	prompt_user black python && python3 -m pip install black-with-tabs
fi
if ! command -v isort >/dev/null; then
	prompt_user isort python && python3 -m pip install isort
fi
if ! command -v clang-format >/dev/null; then
	if prompt_user clang-format C; then
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

# TODO: Find a way to make this POSIX compliant.
shopt -s globstar nullglob

SCR_PATH=$(cd "$(dirname "$0")" && pwd)

for FILE in "$SCR_PATH"/**/*; do
	# Ignore git ignored files
	>/dev/null git check-ignore "$FILE" && continue

	case $FILE in
	*.[ch])
		clang-format -i --verbose --sort-includes -style=file "$FILE"
		;;
	*.py)
		echo Formatting "$FILE"
		>/dev/null isort "$FILE"
		2>/dev/null python3.9 -m black -q -l 100 "$FILE"
		;;
	*.sh)
		echo Formatting "$FILE"
		unexpand -t 8 --first-only "$FILE" >temp
		mv temp "$FILE"
		chmod +x "$FILE"
		;;
	esac
done
