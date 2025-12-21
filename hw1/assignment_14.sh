#!/bin/bash

while true; do
    echo "--- Process Manager ---"
    echo "1. Show my processes"
    echo "2. Find process by name"
    echo "3. Kill process by PID"
    echo "4. Resource consumption"
    echo "5. Exit"
    read -p "Choice: " CHOICE

    case $CHOICE in
        1) ps -u $USER ;;
        2) read -p "Name: " NAME; pgrep -l $NAME ;;
        3) read -p "PID: " PID; kill $PID && echo "Sent SIGTERM to $PID" ;;
        4) top -b -n 1 -u $USER | head -n 20 ;;
        5) exit 0 ;;
        *) echo "Invalid option" ;;
    esac
    echo ""
done