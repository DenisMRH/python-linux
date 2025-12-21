# News Aggregation System

Система для сбора новостей из RSS-лент с возможностью настройки правил выгрузки.

## Структура проекта

- `main.py` - FastAPI приложение с API эндпоинтами
- `database.py` - Модели базы данных (SQLAlchemy)
- `models.py` - Pydantic модели для API
- `fetch_news.py` - Скрипт для выгрузки новостей (запускается через cron)
- `init_data.py` - Скрипт для инициализации БД с начальными данными
- `requirements.txt` - Зависимости проекта

## Установка

1. Установить зависимости:
```bash
pip install -r requirements.txt
```

2. Инициализировать базу данных:
```bash
python init_data.py
```

3. Запустить API сервер:
```bash
uvicorn main:app --host 0.0.0.0 --port 9000
```

## Настройка cron

Добавить в crontab (запуск каждые 30 минут):
```bash
*/30 * * * * cd /path/to/project && /usr/bin/python3 fetch_news.py >> /path/to/project/fetch.log 2>&1
```

Или через команду:
```bash
crontab -e
```

## API Эндпоинты

### Административные (управление источниками)
- `POST /api/admin/sources` - Создать источник
- `GET /api/admin/sources` - Получить все источники
- `GET /api/admin/sources/{id}` - Получить источник по ID
- `PUT /api/admin/sources/{id}` - Обновить источник
- `DELETE /api/admin/sources/{id}` - Удалить источник

### Административные (управление правилами)
- `POST /api/admin/rules` - Создать правило
- `GET /api/admin/rules` - Получить все правила
- `GET /api/admin/rules/{id}` - Получить правило по ID
- `PUT /api/admin/rules/{id}` - Обновить правило
- `DELETE /api/admin/rules/{id}` - Удалить правило

### Работа с новостями
- `GET /api/news` - Получить новости (с фильтрами: category, region, hours, days, limit)
- `GET /api/news/today` - Новости за сегодня
- `GET /api/news/hour` - Новости за последний час
- `GET /api/news/{id}` - Получить новость по ID

## Документация API

После запуска сервера доступна автоматическая документация:
- Swagger UI: http://localhost:9000/docs
- ReDoc: http://localhost:9000/redoc

