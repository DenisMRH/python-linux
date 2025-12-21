#!/bin/bash

N=$1

if ! [[ "$N" =~ ^[0-9]+$ ]] || [ "$N" -le 0 ]; then
    echo "Error: Please provide a positive integer."
    exit 1
fi

for (( i=0; i<N; i++ )); do
    for (( j=0; j<N; j++ )); do
        if [ $i -eq $j ]; then
            printf "1    "
        else
            printf "0    "
        fi
    done
    echo ""
done