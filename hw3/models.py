from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FeedSourceCreate(BaseModel):
    name: str
    url: str
    category: Optional[str] = None
    region: Optional[str] = None


class FeedSourceResponse(BaseModel):
    id: int
    name: str
    url: str
    category: Optional[str]
    region: Optional[str]
    
    class Config:
        from_attributes = True


class FeedRuleCreate(BaseModel):
    name: str
    category: Optional[str] = None
    region: Optional[str] = None
    source_id: int


class FeedRuleUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    region: Optional[str] = None
    source_id: Optional[int] = None


class FeedRuleResponse(BaseModel):
    id: int
    name: str
    category: Optional[str]
    region: Optional[str]
    source_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class NewsItemResponse(BaseModel):
    id: int
    title: str
    description: str
    category: Optional[str]
    region: Optional[str]
    published_at: datetime
    fetched_at: datetime
    source_id: int
    link: str
    
    class Config:
        from_attributes = True

