from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional
import uuid

class SourceOut(BaseModel):
    id: int
    name: str
    url: str
    category: Optional[str]
    model_config = {"from_attributes": True}

class NewsItemOut(BaseModel):
    id: uuid.UUID
    title: str
    url: str
    summary: Optional[str]
    tags: Optional[list[str]]
    image_url: Optional[str]
    author: Optional[str]
    published_at: Optional[datetime]
    source: SourceOut
    is_favorited: bool = False
    model_config = {"from_attributes": True}

class NewsItemDetail(NewsItemOut):
    content: Optional[str]
    linkedin_caption: Optional[str]
    email_caption: Optional[str]

class FavoriteOut(BaseModel):
    id: uuid.UUID
    news_item: NewsItemOut
    created_at: datetime
    model_config = {"from_attributes": True}

class BroadcastRequest(BaseModel):
    news_item_id: uuid.UUID
    channel: str        # email | linkedin | whatsapp
    recipient: Optional[str] = None

class BroadcastResponse(BaseModel):
    id: uuid.UUID
    channel: str
    status: str
    message: str
    preview: Optional[str]

class PaginatedNews(BaseModel):
    items: list[NewsItemOut]
    total: int
    page: int
    per_page: int
    has_more: bool