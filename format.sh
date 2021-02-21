#!/usr/bin/env sh

for FILE in $(find ./* | grep '\.py$'); do
	isort "$FILE" >/dev/null 2>&1
	black -l 80 "$FILE" >/dev/null 2>&1
	echo "Formatting $FILE"
done

for FILE in $(find ./* | grep '\.[ch]$'); do
	clang-format -i --verbose --sort-includes -style=file "$FILE"
done
