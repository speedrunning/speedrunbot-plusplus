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
		isort "$FILE" &>/dev/null
		python3.9 -m black -l 80 "$FILE" &>/dev/null
		echo "Formatting $FILE"
		;;
	*.sh)
		echo "Formatting $FILE"
		unexpand -t 8 --first-only "$FILE" >temp
		mv temp "$FILE"
		chmod +x "$FILE"
		;;
	esac
done
