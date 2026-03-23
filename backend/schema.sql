CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =========================
-- SOURCES TABLE
-- =========================
CREATE TABLE IF NOT EXISTS sources (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    url VARCHAR(500) UNIQUE NOT NULL,
    category VARCHAR(100) DEFAULT 'general',
    is_active BOOLEAN DEFAULT TRUE,
    last_fetched_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- NEWS ITEMS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS news_items (
    id SERIAL PRIMARY KEY,
    source_id INTEGER REFERENCES sources(id) ON DELETE SET NULL,

    title VARCHAR(500) NOT NULL,
    url VARCHAR(1000) UNIQUE NOT NULL,

    url_hash VARCHAR(64) UNIQUE NOT NULL,

    content TEXT,
    summary TEXT,

    image_url VARCHAR(1000),
    author VARCHAR(200),

    published_at TIMESTAMP,
    category VARCHAR(100),

    tags JSONB DEFAULT '[]'::jsonb,  -- FIXED

    ai_processed BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- FAVORITES TABLE
-- =========================
CREATE TABLE IF NOT EXISTS favorites (
    id SERIAL PRIMARY KEY,
    news_item_id INTEGER REFERENCES news_items(id) ON DELETE CASCADE,

    user_session VARCHAR(100) DEFAULT 'default',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(news_item_id, user_session)
);

-- =========================
-- BROADCAST LOGS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS broadcast_logs (
    id SERIAL PRIMARY KEY,

    news_item_id INTEGER REFERENCES news_items(id) ON DELETE CASCADE,

    platform VARCHAR(50) NOT NULL CHECK (platform IN ('email', 'linkedin', 'whatsapp')),  -- FIXED

    status VARCHAR(50) DEFAULT 'pending',

    caption TEXT,
    recipient VARCHAR(200),
    error_message TEXT,

    sent_at TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- USERS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,

    session_id VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(200),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- INDEXES
-- =========================
CREATE INDEX IF NOT EXISTS idx_news_items_created_at 
ON news_items(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_news_items_source_id 
ON news_items(source_id);

CREATE INDEX IF NOT EXISTS idx_news_items_ai_processed 
ON news_items(ai_processed);

CREATE INDEX IF NOT EXISTS idx_news_items_url_hash 
ON news_items(url_hash);

CREATE INDEX IF NOT EXISTS idx_favorites_user_session 
ON favorites(user_session);

CREATE INDEX IF NOT EXISTS idx_broadcast_logs_platform 
ON broadcast_logs(platform);
