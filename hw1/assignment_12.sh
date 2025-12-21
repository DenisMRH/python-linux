#!/bin/bash


# ./assignment_12.sh - игра без ограничения
# ./assignment_12.sh 3  - игра до 3 побед

# Если аргумент не передан, GOAL = 0 (игра без ограничений)
GOAL=${1:-0}
USER_SCORE=0
COMP_SCORE=0
OPTIONS=("rock" "paper" "scissors")

echo "Welcome to Rock-Paper-Scissors!"
[ $GOAL -gt 0 ] && echo "First to $GOAL wins!"

while true; do
    read -p "Your choice (rock/paper/scissors/new/quit): " USER_CHOICE
    # Выход из игры
    [ "$USER_CHOICE" == "quit" ] && break
    # Начать новую игру
    [ "$USER_CHOICE" == "new" ] && USER_SCORE=0 && COMP_SCORE=0 && echo "New game started!" && continue
    
    # Проверяем что юзер ввёл правильный вариант
    if [[ ! " ${OPTIONS[@]} " =~ " ${USER_CHOICE} " ]]; then
        echo "Invalid choice!"
        continue
    fi
    
    # Компьютер выбирает случайный вариант
    COMP_CHOICE=${OPTIONS[$(( RANDOM % 3 ))]}
    echo "Computer chose: $COMP_CHOICE"
    
    # Определяем победителя раунда
    if [ "$USER_CHOICE" == "$COMP_CHOICE" ]; then
        echo "Draw!"
    elif [[ ("$USER_CHOICE" == "rock" && "$COMP_CHOICE" == "scissors") || \
            ("$USER_CHOICE" == "paper" && "$COMP_CHOICE" == "rock") || \
            ("$USER_CHOICE" == "scissors" && "$COMP_CHOICE" == "paper") ]]; then
        echo "You win this round!"
        USER_SCORE=$((USER_SCORE + 1))
    else
        echo "Computer wins this round!"
        COMP_SCORE=$((COMP_SCORE + 1))
    fi
    
    echo "Score: You $USER_SCORE - $COMP_SCORE Computer"
    
    # Проверяем достигнута ли цель
    if [ $GOAL -gt 0 ]; then
        if [ $USER_SCORE -eq $GOAL ]; then
            echo "CONGRATULATIONS! YOU WON THE GAME!"
            break
        elif [ $COMP_SCORE -eq $GOAL ]; then
            echo "GAME OVER! COMPUTER WON THE GAME!"
            break
        fi
    fi
done