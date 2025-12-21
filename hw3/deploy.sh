#!/bin/bash
# Скрипт для развертывания на виртуальной машине

# Создаем директорию проекта
PROJECT_DIR="$HOME/news_aggregation"
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# Создаем виртуальное окружение Python
python3 -m venv venv
source venv/bin/activate

# Устанавливаем зависимости
pip install --upgrade pip
pip install -r requirements.txt

# Инициализируем базу данных
python3 init_data.py

# Делаем скрипт выгрузки исполняемым
chmod +x fetch_news.py

echo "Deployment completed!"
echo "To start the server, run:"
echo "  source venv/bin/activate"
echo "  uvicorn main:app --host 0.0.0.0 --port 9000"

