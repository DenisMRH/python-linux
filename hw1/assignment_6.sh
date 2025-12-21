#!/bin/bash

N=${1:-5}

if ! [[ "$N" =~ ^[0-9]+$ ]] || [ "$N" -le 0 ]; then
    echo "Error: you should use a positive integer as an argument"
    exit 1
fi

for (( i=0; i<N; i++ )); do
    val=1
    for (( j=0; j<=i; j++ )); do
        printf "%d    " "$val"
        val=$(( val * (i - j) / (j + 1) ))
    done
    echo ""
done