from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime, timedelta
from typing import Optional, List
import database
import models

app = FastAPI(title="News Aggregation System", version="1.0.0")

database.init_db()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/api/admin/sources", response_model=models.FeedSourceResponse)
def create_source(source: models.FeedSourceCreate, db: Session = Depends(get_db)):
    """Создать новый источник RSS-ленты"""
    db_source = database.FeedSource(**source.dict())
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source


@app.get("/api/admin/sources", response_model=List[models.FeedSourceResponse])
def get_sources(db: Session = Depends(get_db)):
    """Получить все источники"""
    return db.query(database.FeedSource).all()


@app.get("/api/admin/sources/{source_id}", response_model=models.FeedSourceResponse)
def get_source(source_id: int, db: Session = Depends(get_db)):
    """Получить источник по ID"""
    source = db.query(database.FeedSource).filter(database.FeedSource.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@app.put("/api/admin/sources/{source_id}", response_model=models.FeedSourceResponse)
def update_source(source_id: int, source: models.FeedSourceCreate, db: Session = Depends(get_db)):
    """Обновить источник"""
    db_source = db.query(database.FeedSource).filter(database.FeedSource.id == source_id).first()
    if not db_source:
        raise HTTPException(status_code=404, detail="Source not found")
    
    for key, value in source.dict().items():
        setattr(db_source, key, value)
    
    db.commit()
    db.refresh(db_source)
    return db_source


@app.delete("/api/admin/sources/{source_id}")
def delete_source(source_id: int, db: Session = Depends(get_db)):
    """Удалить источник"""
    db_source = db.query(database.FeedSource).filter(database.FeedSource.id == source_id).first()
    if not db_source:
        raise HTTPException(status_code=404, detail="Source not found")
    
    db.delete(db_source)
    db.commit()
    return {"message": "Source deleted successfully"}



@app.post("/api/admin/rules", response_model=models.FeedRuleResponse)
def create_rule(rule: models.FeedRuleCreate, db: Session = Depends(get_db)):
    """Создать новое правило выгрузки"""
    # Проверяем, что источник существует
    source = db.query(database.FeedSource).filter(database.FeedSource.id == rule.source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    
    db_rule = database.FeedRule(**rule.dict())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule


@app.get("/api/admin/rules", response_model=List[models.FeedRuleResponse])
def get_rules(db: Session = Depends(get_db)):
    """Получить все правила"""
    return db.query(database.FeedRule).all()


@app.get("/api/admin/rules/{rule_id}", response_model=models.FeedRuleResponse)
def get_rule(rule_id: int, db: Session = Depends(get_db)):
    """Получить правило по ID"""
    rule = db.query(database.FeedRule).filter(database.FeedRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return rule


@app.put("/api/admin/rules/{rule_id}", response_model=models.FeedRuleResponse)
def update_rule(rule_id: int, rule: models.FeedRuleUpdate, db: Session = Depends(get_db)):
    """Обновить правило"""
    db_rule = db.query(database.FeedRule).filter(database.FeedRule.id == rule_id).first()
    if not db_rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    # Проверяем источник, если он указан
    if rule.source_id is not None:
        source = db.query(database.FeedSource).filter(database.FeedSource.id == rule.source_id).first()
        if not source:
            raise HTTPException(status_code=404, detail="Source not found")
    
    for key, value in rule.dict(exclude_unset=True).items():
        setattr(db_rule, key, value)
    
    db_rule.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_rule)
    return db_rule


@app.delete("/api/admin/rules/{rule_id}")
def delete_rule(rule_id: int, db: Session = Depends(get_db)):
    """Удалить правило"""
    db_rule = db.query(database.FeedRule).filter(database.FeedRule.id == rule_id).first()
    if not db_rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    db.delete(db_rule)
    db.commit()
    return {"message": "Rule deleted successfully"}



@app.get("/api/news", response_model=List[models.NewsItemResponse])
def get_news(
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    region: Optional[str] = Query(None, description="Фильтр по региону"),
    hours: Optional[int] = Query(None, description="Новости за последние N часов"),
    days: Optional[int] = Query(None, description="Новости за последние N дней"),
    limit: int = Query(100, description="Лимит новостей"),
    db: Session = Depends(get_db)
):
    """Получить новости с фильтрами"""
    query = db.query(database.NewsItem)
    
    if category:
        query = query.filter(database.NewsItem.category == category)
    
    if region:
        query = query.filter(database.NewsItem.region == region)
    
    if hours:
        time_threshold = datetime.utcnow() - timedelta(hours=hours)
        query = query.filter(database.NewsItem.published_at >= time_threshold)
    elif days:
        time_threshold = datetime.utcnow() - timedelta(days=days)
        query = query.filter(database.NewsItem.published_at >= time_threshold)
    
    query = query.order_by(database.NewsItem.published_at.desc())
    
    return query.limit(limit).all()


@app.get("/api/news/today", response_model=List[models.NewsItemResponse])
def get_news_today(
    category: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    limit: int = Query(100),
    db: Session = Depends(get_db)
):
    """Получить новости за сегодня"""
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    query = db.query(database.NewsItem).filter(database.NewsItem.published_at >= today_start)
    
    if category:
        query = query.filter(database.NewsItem.category == category)
    if region:
        query = query.filter(database.NewsItem.region == region)
    
    return query.order_by(database.NewsItem.published_at.desc()).limit(limit).all()


@app.get("/api/news/hour", response_model=List[models.NewsItemResponse])
def get_news_last_hour(
    category: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    limit: int = Query(100),
    db: Session = Depends(get_db)
):
    """Получить новости за последний час"""
    hour_ago = datetime.utcnow() - timedelta(hours=1)
    query = db.query(database.NewsItem).filter(database.NewsItem.published_at >= hour_ago)
    
    if category:
        query = query.filter(database.NewsItem.category == category)
    if region:
        query = query.filter(database.NewsItem.region == region)
    
    return query.order_by(database.NewsItem.published_at.desc()).limit(limit).all()


@app.get("/api/news/{news_id}", response_model=models.NewsItemResponse)
def get_news_item(news_id: int, db: Session = Depends(get_db)):
    """Получить новость по ID"""
    news = db.query(database.NewsItem).filter(database.NewsItem.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News item not found")
    return news


@app.get("/")
def root():
    """Корневой эндпоинт"""
    return {
        "message": "News Aggregation System API",
        "docs": "/docs",
        "admin": {
            "sources": "/api/admin/sources",
            "rules": "/api/admin/rules"
        },
        "news": {
            "all": "/api/news",
            "today": "/api/news/today",
            "hour": "/api/news/hour"
        }
    }

