#!/bin/bash

TARGET=$(( RANDOM % 101 ))
ATTEMPTS=0
MAX_ATTEMPTS=10

echo "I've picked a number between 0 and 100. You have $MAX_ATTEMPTS tries."

while [ $ATTEMPTS -lt $MAX_ATTEMPTS ]; do
    read -p "Enter your guess: " GUESS
    
    if ! [[ "$GUESS" =~ ^[0-9]+$ ]]; then
        echo "Please enter a valid number."
        continue
    fi
    
    ATTEMPTS=$(( ATTEMPTS + 1 ))
    
    if [ "$GUESS" -eq "$TARGET" ]; then
        echo "Congratulations! You guessed it in $ATTEMPTS attempts."
        exit 0
    elif [ "$GUESS" -lt "$TARGET" ]; then
        echo "Greater..."
    else
        echo "Lower..."
    fi
done

echo "Game over! You've used all attempts. The number was $TARGET."