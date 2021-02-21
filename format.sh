#!/usr/bin/env sh

for FILE in $(find ./* | grep '\.py$'); do
    isort "$FILE" >/dev/null 2>&1
    black "$FILE" >/dev/null 2>&1
    echo "Formatted $FILE"
done
