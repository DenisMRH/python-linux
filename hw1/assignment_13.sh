#!/bin/bash

WORD_FILE=$1
if [ ! -f "$WORD_FILE" ]; then
    echo "Error: words file not found."
    exit 1
fi

WINS=0
LOSSES=0

while true; do
    SECRET=$(shuf -n 1 "$WORD_FILE" | tr '[:upper:]' '[:lower:]')
    LENGTH=${#SECRET}
    GUESSED_DISPLAY=$(printf '_%.0s' $(seq 1 $LENGTH))
    LIVES=6
    USED_LETTERS=""

    echo "Welcome to Hangman! The word has $LENGTH letters."
    echo "Current score: Wins: $WINS, Losses: $LOSSES"

    while [ $LIVES -gt 0 ] && [[ "$GUESSED_DISPLAY" == *"_"* ]]; do
        echo "----------------------------"
        echo "Word: $GUESSED_DISPLAY"
        echo "Lives: $LIVES | Used: $USED_LETTERS"
        read -p "Guess a letter: " LETTER
        LETTER=$(echo $LETTER | tr '[:upper:]' '[:lower:]')

        if [[ "$USED_LETTERS" == *"$LETTER"* ]]; then
            echo "You already tried '$LETTER'!"
            continue
        fi
        
        USED_LETTERS+="$LETTER "

        if [[ "$SECRET" == *"$LETTER"* ]]; then
            echo "Good job!"
            NEW_DISPLAY=""
            for (( i=0; i<$LENGTH; i++ )); do
                char=${SECRET:$i:1}
                if [ "$char" == "$LETTER" ]; then
                    NEW_DISPLAY+="$LETTER"
                else
                    NEW_DISPLAY+="${GUESSED_DISPLAY:$i:1}"
                fi
            done
            GUESSED_DISPLAY=$NEW_DISPLAY
        else
            echo "Wrong!"
            LIVES=$((LIVES - 1))
        fi
    done

    if [[ "$GUESSED_DISPLAY" != *"_"* ]]; then
        echo "Winner! The word was: $SECRET"
        WINS=$((WINS + 1))
    else
        echo "You lost! The word was: $SECRET"
        LOSSES=$((LOSSES + 1))
    fi

    echo "Score: Wins: $WINS, Losses: $LOSSES"
    read -p "Play again? (y/n): " PLAY_AGAIN
    if [ "$PLAY_AGAIN" != "y" ] && [ "$PLAY_AGAIN" != "Y" ]; then
        echo "Thanks for playing! Final score: Wins: $WINS, Losses: $LOSSES"
        break
    fi
    echo ""
done