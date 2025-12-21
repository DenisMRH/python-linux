#!/bin/bash
# Скрипт для создания всех файлов проекта на сервере
# Запустите этот скрипт на сервере после подключения по SSH

cd ~/news_aggregation || mkdir -p ~/news_aggregation && cd ~/news_aggregation

# Создаем requirements.txt
cat > requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
feedparser==6.0.10
pydantic==2.5.0
python-dateutil==2.8.2
EOF

echo "Files will be created. Please copy the content of each file from your local machine."
echo "Or use scp to copy files from local machine."

