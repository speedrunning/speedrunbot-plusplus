#!/usr/bin/env bash

shopt -s globstar nullglob

SCR_PATH=$(cd "$(dirname "$0")" && pwd)

for FILE in "$SCR_PATH"/**/*.py; do
    isort "$FILE" >/dev/null 2>&1
    black -l 80 "$FILE" >/dev/null 2>&1
    echo "Formatting $FILE"
done

for FILE in "$SCR_PATH"**/*.[ch]; do
    clang-format -i --verbose --sort-includes -style=file "$FILE"
done
