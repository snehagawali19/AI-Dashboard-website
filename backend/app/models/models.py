import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, Boolean, Integer, ForeignKey,
    TIMESTAMP, UniqueConstraint, Index
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB, FLOAT
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255))
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    favorites = relationship("Favorite", back_populates="user")

class Source(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    url = Column(Text, nullable=False, unique=True)
    type = Column(String(50), nullable=False)       # rss | api | scrape
    category = Column(String(100))
    active = Column(Boolean, default=True)
    last_fetched_at = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    news_items = relationship("NewsItem", back_populates="source")

class NewsItem(Base):
    __tablename__ = "news_items"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    title = Column(Text, nullable=False)
    url = Column(Text, nullable=False, unique=True)
    content = Column(Text)
    summary = Column(Text)
    linkedin_caption = Column(Text)
    email_caption = Column(Text)
    tags = Column(ARRAY(Text))
    image_url = Column(Text)
    author = Column(String(255))
    published_at = Column(TIMESTAMP(timezone=True))
    url_hash = Column(String(64), nullable=False, unique=True)
    embedding = Column(ARRAY(FLOAT))
    ai_processed = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    source = relationship("Source", back_populates="news_items")
    favorites = relationship("Favorite", back_populates="news_item")

class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = (UniqueConstraint("user_id", "news_item_id"),)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    news_item_id = Column(UUID(as_uuid=True), ForeignKey("news_items.id",
                          ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    user = relationship("User", back_populates="favorites")
    news_item = relationship("NewsItem", back_populates="favorites")

class BroadcastLog(Base):
    __tablename__ = "broadcast_logs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    news_item_id = Column(UUID(as_uuid=True), ForeignKey("news_items.id"))
    channel = Column(String(50), nullable=False)    # email | linkedin | whatsapp
    status = Column(String(50), default="sent")
    payload = Column(JSONB)
    sent_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)