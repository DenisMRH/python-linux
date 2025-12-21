#!/bin/bash

ARCHIVE_NAME="$HOME/my_backup_$(date +%Y%m%d_%H%M%S).tar.gz"
VALID_FILES=()

for file in "$@"; do
    if [ -f "$file" ]; then
        VALID_FILES+=("$file")
    else
        echo "Warning: File '$file' not found. Skipping."
    fi
done

if [ ${#VALID_FILES[@]} -eq 0 ]; then
    echo "Error: No valid files to archive."
    exit 1
fi

tar -czf "$ARCHIVE_NAME" "${VALID_FILES[@]}"
echo "Archive created: $ARCHIVE_NAME"