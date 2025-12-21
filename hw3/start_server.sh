#!/bin/bash
# Скрипт для запуска сервера

PROJECT_DIR="$HOME/news_aggregation"
cd $PROJECT_DIR

source venv/bin/activate

# Запускаем сервер на порту 9000 (измените на нужный порт)
uvicorn main:app --host 0.0.0.0 --port 9000

