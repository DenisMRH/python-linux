#!/usr/bin/env python3
"""
Скрипт для выгрузки новостей из RSS-лент на основе правил
Запускается по расписанию через cron
"""

import feedparser
import database
from sqlalchemy.orm import Session
from datetime import datetime
import sys


def parse_date(date_str):
    """Парсинг даты из RSS"""
    try:
        # feedparser возвращает struct_time, конвертируем в datetime
        if hasattr(date_str, 'timetuple'):
            return datetime(*date_str.timetuple()[:6])
        return datetime.utcnow()
    except:
        return datetime.utcnow()


def fetch_news_from_source(source: database.FeedSource, db: Session):
    """Выгрузка новостей из одного источника"""
    try:
        print(f"Fetching news from {source.name} ({source.url})")
        feed = feedparser.parse(source.url)
        
        if feed.bozo and feed.bozo_exception:
            print(f"Error parsing feed {source.url}: {feed.bozo_exception}")
            return 0
        
        count = 0
        for entry in feed.entries:
            try:
                # Проверяем, не существует ли уже эта новость
                existing = db.query(database.NewsItem).filter(
                    database.NewsItem.link == entry.link
                ).first()
                
                if existing:
                    continue  # Пропускаем дубликаты
                
                # Парсим дату публикации
                published_at = parse_date(entry.get('published_parsed', datetime.utcnow()))
                
                # Создаем новость
                news_item = database.NewsItem(
                    title=entry.get('title', ''),
                    description=entry.get('description', '') or entry.get('summary', ''),
                    category=source.category,
                    region=source.region,
                    published_at=published_at,
                    source_id=source.id,
                    link=entry.link
                )
                
                db.add(news_item)
                count += 1
            except Exception as e:
                print(f"Error processing entry: {e}")
                continue
        
        db.commit()
        print(f"Fetched {count} new items from {source.name}")
        return count
        
    except Exception as e:
        print(f"Error fetching from {source.name}: {e}")
        db.rollback()
        return 0


def fetch_news_by_rules():
    """Выгрузка новостей на основе правил"""
    db = database.SessionLocal()
    try:
        # Получаем все активные правила
        rules = db.query(database.FeedRule).all()
        
        if not rules:
            print("No rules found. Please create rules first.")
            return
        
        total_fetched = 0
        sources_processed = set()
        
        # Для каждого правила получаем источник и выгружаем новости
        for rule in rules:
            source = db.query(database.FeedSource).filter(
                database.FeedSource.id == rule.source_id
            ).first()
            
            if not source:
                print(f"Warning: Source {rule.source_id} not found for rule {rule.name}")
                continue
            
            # Обрабатываем каждый источник только один раз
            if source.id not in sources_processed:
                fetched = fetch_news_from_source(source, db)
                total_fetched += fetched
                sources_processed.add(source.id)
        
        print(f"Total fetched: {total_fetched} news items")
        
    except Exception as e:
        print(f"Error in fetch_news_by_rules: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    fetch_news_by_rules()

