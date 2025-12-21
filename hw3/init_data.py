#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных с начальными данными
"""

import database
from datetime import datetime

database.init_db()

db = database.SessionLocal()

sources_data = [
    {"name": "Интерфакс", "url": "https://www.interfax.ru/rss.asp", "category": "общие", "region": None},
    {"name": "Газета Коммерсант", "url": "https://www.kommersant.ru/RSS/main.xml", "category": "общие", "region": None},
    {"name": "Коммерсант-Наука", "url": "https://www.kommersant.ru/RSS/science.xml", "category": "наука", "region": None},
    {"name": "Коммерсант-Политика", "url": "https://www.kommersant.ru/RSS/section-politics.xml", "category": "политика", "region": None},
    {"name": "МК-Политика", "url": "https://www.mk.ru/rss/politics/index.xml", "category": "политика", "region": None},
    {"name": "МК-Наука", "url": "https://www.mk.ru/rss/science/index.xml", "category": "наука", "region": None},
    {"name": "Коммерсант-СПБ", "url": "https://www.kommersant.ru/rss/regions/piter_all.xml", "category": None, "region": "СПБ"},
    {"name": "АИФ-СПБ", "url": "https://spb.aif.ru/rss/all.php", "category": None, "region": "СПБ"},
    {"name": "АИФ-РЗН", "url": "https://rzn.aif.ru/rss/all.php", "category": None, "region": "РЗН"},
    {"name": "Инфо-РЗН", "url": "https://rss.rzn.info/rss/news/ryazan.xml", "category": None, "region": "РЗН"},
]

print("Adding feed sources...")
for source_data in sources_data:
    existing = db.query(database.FeedSource).filter(
        database.FeedSource.url == source_data["url"]
    ).first()
    
    if not existing:
        source = database.FeedSource(**source_data)
        db.add(source)
        print(f"Added: {source_data['name']}")
    else:
        print(f"Already exists: {source_data['name']}")

db.commit()

rules_data = [
    {"name": "Новости политики", "category": "политика", "region": None, "source_name": "МК-Политика"},
    {"name": "Новости по Санкт-Петербургу", "category": None, "region": "СПБ", "source_name": "АИФ-СПБ"},
    {"name": "Общие новости - Интерфакс", "category": "общие", "region": None, "source_name": "Интерфакс"},
    {"name": "Общие новости - Коммерсант", "category": "общие", "region": None, "source_name": "Газета Коммерсант"},
]

print("\nAdding feed rules...")
for rule_data in rules_data:
    source_name = rule_data.pop("source_name")
    source = db.query(database.FeedSource).filter(
        database.FeedSource.name == source_name
    ).first()
    
    if source:
        existing_rule = db.query(database.FeedRule).filter(
            database.FeedRule.name == rule_data["name"]
        ).first()
        
        if not existing_rule:
            rule = database.FeedRule(
                name=rule_data["name"],
                category=rule_data["category"],
                region=rule_data["region"],
                source_id=source.id
            )
            db.add(rule)
            print(f"Added rule: {rule_data['name']} -> {source_name}")
        else:
            print(f"Rule already exists: {rule_data['name']}")
    else:
        print(f"Source not found: {source_name}")

db.commit()
db.close()

print("\nInitialization complete!")

