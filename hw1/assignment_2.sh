#!/bin/bash

FILE_PATH=$1

count=$(wc -w < "$FILE_PATH")

count=$(echo $count | xargs)

echo "Words count: $count"