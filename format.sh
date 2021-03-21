#!/usr/bin/env bash

# Format all the source files.

shopt -s globstar nullglob

SCR_PATH=$(cd "$(dirname "$0")" && pwd)

for FILE in "$SCR_PATH"/**/*; do
	case $FILE in
	*.[ch])
		clang-format -i --verbose --sort-includes -style=file "$FILE"
		;;
	*.py)
		echo "Formatting $FILE"
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
		echo "Formatting $FILE"
		unexpand -t 8 --first-only "$FILE" >temp
		mv temp "$FILE"
		chmod +x "$FILE"
		;;
	esac
done
