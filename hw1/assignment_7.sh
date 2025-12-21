#!/bin/bash

FILE=$1

if [ ! -f "$FILE" ]; then
    echo "Error: File not found"
    exit 1
fi

echo "Lines count: $(wc -l < "$FILE" | xargs)"
echo "Words count: $(wc -w < "$FILE" | xargs)"

longest=$(tr -s '[:space:]' '\n' < "$FILE" | awk '{ if (length($0) > max) {max=length($0); word=$0} } END { print word }')
echo "Longest word: $longest"

echo "Word frequency:"
tr -s '[:space:]' '\n' < "$FILE" | sed 's/[[:punct:]]//g' | sort | uniq -c | sort -nr