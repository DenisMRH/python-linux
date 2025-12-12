"""
Простой скрипт для тестирования jokes_app.
Использование: python test_jokes.py
"""

import sys
import io

# Устанавливаем UTF-8 для вывода в консоль Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import httpx
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8001"


def print_joke(joke, index=None):
    """Красиво выводит анекдот."""
    if index is not None:
        print(f"\n{'='*60}")
        print(f"Анекдот #{index + 1}")
    else:
        print(f"\n{'='*60}")
    print(f"Текст: {joke['text']}")
    print(f"Рейтинг: {joke['rating']}")
    if joke.get('autor_profile'):
        print(f"Автор: {joke['autor_profile']}")


def test_random():
    """Тестирует эндпоинт /random."""
    print("\n" + "="*60)
    print("ТЕСТ: /random - Случайные анекдоты")
    print("="*60)
    
    try:
        response = httpx.get(f"{BASE_URL}/random", timeout=30.0)
        response.raise_for_status()
        jokes = response.json()
        
        print(f"\nПолучено анекдотов: {len(jokes)}\n")
        
        for i, joke in enumerate(jokes[:5]):  # Показываем первые 5
            print_joke(joke, i)
        
    except Exception as e:
        print(f"Ошибка: {e}")


def test_best():
    """Тестирует эндпоинт /best."""
    print("\n" + "="*60)
    print("ТЕСТ: /best - Лучшие анекдоты за день")
    print("="*60)
    
    # Используем сегодняшнюю дату или вчерашнюю (на случай если сегодня еще нет данных)
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    test_date = yesterday.strftime("%d-%B-%Y")  # Формат: 01-January-2025
    
    print(f"\nЗапрашиваем анекдоты за: {test_date}")
    
    try:
        response = httpx.get(f"{BASE_URL}/best", params={"day": test_date}, timeout=30.0)
        response.raise_for_status()
        jokes = response.json()
        
        print(f"\nПолучено лучших анекдотов: {len(jokes)}\n")
        
        for i, joke in enumerate(jokes[:5]):  # Показываем первые 5
            print_joke(joke, i)
        
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    print("\n" + "Тестирование jokes_app" + "\n")
    
    test_random()
    test_best()
    
    print("\n" + "="*60)
    print("Тестирование завершено!")
    print("="*60 + "\n")

