#!/usr/bin/env bash

# Format all the source files.

shopt -s globstar nullglob

SCR_PATH=$(cd "$(dirname "$0")" && pwd)

for FILE in "$SCR_PATH"/**/*.py; do
	isort "$FILE" &>/dev/null
	python3.9 -m black -l 80 "$FILE" &>/dev/null
	echo "Formatting $FILE"
done

for FILE in "$SCR_PATH"**/*.[ch]; do
	clang-format -i --verbose --sort-includes -style=file "$FILE"
done
