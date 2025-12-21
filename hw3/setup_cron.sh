#!/bin/bash
# Скрипт для настройки cron задачи

PROJECT_DIR="$HOME/news_aggregation"
PYTHON_PATH="$PROJECT_DIR/venv/bin/python3"
SCRIPT_PATH="$PROJECT_DIR/fetch_news.py"
LOG_PATH="$PROJECT_DIR/fetch.log"

# Добавляем задачу в crontab (каждые 30 минут)
(crontab -l 2>/dev/null; echo "*/30 * * * * cd $PROJECT_DIR && $PYTHON_PATH $SCRIPT_PATH >> $LOG_PATH 2>&1") | crontab -

echo "Cron job added successfully!"
echo "To view cron jobs: crontab -l"
echo "To remove cron job: crontab -e"

