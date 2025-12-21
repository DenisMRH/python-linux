#!/bin/bash

# проверяем передан путь к директории
if [ -z "$1" ]; then
    echo "Usage: $0 /path/to/directory"
    exit 1
fi

SOURCE_DIR=$1
BACKUP_DIR="$HOME/backups"
# создаем папку для бэкапов если вдруг нет
mkdir -p "$BACKUP_DIR"

#  Получаем текущую дату в формате YYYY-MM-DD
DATE=$(date +%Y-%m-%d)
ARCHIVE_NAME="$BACKUP_DIR/backup_$DATE.tar.gz"

# Создаем tar.gz архив с указанныи путём
echo "Creating backup of $SOURCE_DIR..."
tar -czf "$ARCHIVE_NAME" "$SOURCE_DIR"

# Проверяем целостность архива 
# перенаправляю в /dev/null, чтобы не выводить список файлов
if tar -tzf "$ARCHIVE_NAME" > /dev/null; then
    echo "Integrity check passed."
else
    echo "Error: Archive is corrupted!"
    exit 1
fi

# Удаляем архивы старше 7 дней
echo "Cleaning up old backups..."
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +7 -exec rm {} \;

echo "Backup finished successfully."