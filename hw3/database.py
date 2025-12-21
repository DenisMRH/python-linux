from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./news.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class FeedSource(Base):
    """Источники RSS-лент"""
    __tablename__ = "feed_sources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True) 
    url = Column(String, unique=True)  
    category = Column(String, nullable=True)  
    region = Column(String, nullable=True)  
    
    rules = relationship("FeedRule", back_populates="source")


class FeedRule(Base):
    """Правила выгрузки новостей"""
    __tablename__ = "feed_rules"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String) 
    category = Column(String, nullable=True) 
    region = Column(String, nullable=True)  
    source_id = Column(Integer, ForeignKey("feed_sources.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    source = relationship("FeedSource", back_populates="rules")


class NewsItem(Base):
    """Новости"""
    __tablename__ = "news_items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    category = Column(String, index=True, nullable=True)
    region = Column(String, index=True, nullable=True)
    published_at = Column(DateTime, index=True) 
    fetched_at = Column(DateTime, default=datetime.utcnow, index=True) 
    source_id = Column(Integer, ForeignKey("feed_sources.id"))
    link = Column(String, unique=True) 
    
    source = relationship("FeedSource")


def init_db():
    """Инициализация базы данных"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Получение сессии БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

