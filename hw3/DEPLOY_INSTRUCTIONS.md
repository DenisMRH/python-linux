# Инструкция по развертыванию на виртуальной машине

## Шаг 1: Подключение к серверу

```bash
ssh user_55@89.169.185.16
# Пароль: LesaLesa14
```

## Шаг 2: Создание директории проекта

```bash
mkdir -p ~/news_aggregation
cd ~/news_aggregation
```

## Шаг 3: Копирование файлов

Скопируйте все файлы проекта на сервер одним из способов:

### Вариант A: Используя scp с локальной машины (в отдельном терминале)

```bash
cd "C:\Users\Akhrameev Denis\Documents\HSE\python&linux\hw3"
scp main.py database.py models.py fetch_news.py init_data.py requirements.txt deploy.sh setup_cron.sh start_server.sh README.md user_55@89.169.185.16:~/news_aggregation/
```

### Вариант B: Создание файлов напрямую на сервере

Подключитесь по SSH и создайте файлы вручную, скопировав содержимое из локальных файлов.

## Шаг 4: Установка зависимостей

```bash
cd ~/news_aggregation
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Шаг 5: Инициализация базы данных

```bash
python3 init_data.py
```

## Шаг 6: Настройка cron (опционально, для автоматической выгрузки новостей)

```bash
chmod +x setup_cron.sh
./setup_cron.sh
```

Или вручную:
```bash
crontab -e
# Добавьте строку:
*/30 * * * * cd ~/news_aggregation && ~/news_aggregation/venv/bin/python3 ~/news_aggregation/fetch_news.py >> ~/news_aggregation/fetch.log 2>&1
```

## Шаг 7: Запуск сервера

**ВАЖНО:** Используйте порт 9000 + номер вашей строки в таблице. Если номер не указан, используйте 9000.

```bash
# Запуск в текущей сессии (для тестирования)
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 9000

# Или используйте скрипт:
chmod +x start_server.sh
./start_server.sh
```

## Шаг 8: Запуск в фоновом режиме (рекомендуется)

Для постоянной работы сервера используйте `screen` или `tmux`:

```bash
# Установка screen (если не установлен)
sudo apt-get update && sudo apt-get install -y screen

# Создание новой сессии
screen -S news_server

# В сессии запустите:
cd ~/news_aggregation
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 9000

# Отключитесь от сессии: Ctrl+A, затем D
# Вернуться к сессии: screen -r news_server
```

Или используйте systemd service (более надежный вариант):

Создайте файл `/etc/systemd/system/news-aggregation.service`:

```ini
[Unit]
Description=News Aggregation API Service
After=network.target

[Service]
Type=simple
User=user_55
WorkingDirectory=/home/user_55/news_aggregation
Environment="PATH=/home/user_55/news_aggregation/venv/bin"
ExecStart=/home/user_55/news_aggregation/venv/bin/uvicorn main:app --host 0.0.0.0 --port 9000
Restart=always

[Install]
WantedBy=multi-user.target
```

Затем:
```bash
sudo systemctl daemon-reload
sudo systemctl enable news-aggregation
sudo systemctl start news-aggregation
sudo systemctl status news-aggregation
```

## Проверка работы

После запуска сервера проверьте:

1. API доступен: `http://89.169.185.16:9000/`
2. Документация: `http://89.169.185.16:9000/docs`
3. Получить все источники: `http://89.169.185.16:9000/api/admin/sources`
4. Получить все правила: `http://89.169.185.16:9000/api/admin/rules`

## Первая выгрузка новостей

После настройки правил выполните первую выгрузку:

```bash
cd ~/news_aggregation
source venv/bin/activate
python3 fetch_news.py
```

## Полезные команды

- Просмотр логов выгрузки: `tail -f ~/news_aggregation/fetch.log`
- Просмотр новостей через API: `curl http://89.169.185.16:9000/api/news?limit=10`
- Проверка статуса сервиса: `sudo systemctl status news-aggregation`
- Просмотр логов сервиса: `sudo journalctl -u news-aggregation -f`

