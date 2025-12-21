#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "ERROR: please enter numbers"
    exit 1
fi

re='^-?[0-9]+([.][0-9]+)?$'

if ! [[ $1 =~ $re ]] || ! [[ $2 =~ $re ]]; then
    echo "ERROR: please enter numbers"
    exit 1
fi

sum=$(echo "$1 + $2" | bc -l)

sum=$(echo "$sum" | sed 's/\.0*$//;s/\([0-9]\.[0-9]*[1-9]\)0*$/\1/')

echo "The sum is: $sum"