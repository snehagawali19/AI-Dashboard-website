"""
News ingestion from 20+ RSS feeds.
Fetches, parses, normalises, and stores new items.
"""
import hashlib
import logging
import feedparser
import httpx
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models import NewsItem, Source
from app.config import settings

logger = logging.getLogger(__name__)

# ── 20+ AI/Tech RSS sources ────────────────────────────────────────────────
RSS_SOURCES = [
    {"name": "TechCrunch AI",      "url": "https://techcrunch.com/category/artificial-intelligence/feed/", "category": "general"},
    {"name": "VentureBeat AI",     "url": "https://venturebeat.com/ai/feed/",                               "category": "general"},
    {"name": "The Verge AI",       "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml","category": "general"},
    {"name": "Wired AI",           "url": "https://www.wired.com/feed/tag/ai/rss",                          "category": "general"},
    {"name": "MIT Tech Review AI", "url": "https://www.technologyreview.com/feed/",                          "category": "research"},
    {"name": "ArXiv CS.AI",        "url": "https://rss.arxiv.org/rss/cs.AI",                                "category": "research"},
    {"name": "ArXiv CS.LG",        "url": "https://rss.arxiv.org/rss/cs.LG",                                "category": "research"},
    {"name": "Google AI Blog",     "url": "https://blog.research.google/feeds/posts/default",                "category": "research"},
    {"name": "DeepMind Blog",      "url": "https://www.deepmind.com/blog/rss.xml",                          "category": "research"},
    {"name": "Hugging Face",       "url": "https://huggingface.co/blog/feed.xml",                           "category": "tools"},
    {"name": "Towards Data Sci",   "url": "https://towardsdatascience.com/feed",                            "category": "tutorials"},
    {"name": "KDnuggets",          "url": "https://www.kdnuggets.com/feed",                                 "category": "general"},
    {"name": "Analytics Vidhya",   "url": "https://www.analyticsvidhya.com/feed/",                         "category": "tutorials"},
    {"name": "Machine Learning M", "url": "https://machinelearningmastery.com/feed/",                       "category": "tutorials"},
    {"name": "Import AI",          "url": "https://us13.campaign-archive.com/feed?u=67bd06787e84d73db24fb0aa5&id=6c9d98ff2c", "category": "research"},
    {"name": "NVIDIA AI",          "url": "https://blogs.nvidia.com/blog/category/deep-learning/feed/",     "category": "industry"},
    {"name": "Microsoft AI",       "url": "https://blogs.microsoft.com/ai/feed/",                           "category": "industry"},
    {"name": "AWS ML Blog",        "url": "https://aws.amazon.com/blogs/machine-learning/feed/",            "category": "industry"},
    {"name": "OpenAI Blog",        "url": "https://openai.com/news/rss.xml",                                "category": "research"},
    {"name": "Anthropic",          "url": "https://www.anthropic.com/news/rss.xml",                         "category": "research"},
    {"name": "Papers With Code",   "url": "https://paperswithcode.com/latest?format=rss",                  "category": "research"},
    {"name": "AI News (ainews)",   "url": "https://buttondown.email/ainews/rss",                            "category": "general"},
]


def _hash_url(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()


def _parse_date(entry) -> datetime | None:
    for attr in ("published_parsed", "updated_parsed"):
        val = getattr(entry, attr, None)
        if val:
            try:
                return datetime(*val[:6], tzinfo=timezone.utc)
            except Exception:
                pass
    return None


def ensure_sources(db: Session) -> dict[str, Source]:
    """Upsert all configured RSS sources, return url→Source map."""
    existing = {s.url: s for s in db.query(Source).all()}
    for cfg in RSS_SOURCES:
        if cfg["url"] not in existing:
            src = Source(name=cfg["name"], url=cfg["url"],
                         type="rss", category=cfg["category"])
            db.add(src)
            db.flush()
            existing[cfg["url"]] = src
    db.commit()
    return existing


async def fetch_feed(source: Source) -> list[dict]:
    """Parse one RSS feed; return normalised article dicts."""
    items = []
    try:
        feed = feedparser.parse(source.url)
        for entry in feed.entries[:15]:  # cap at 15 per source per run
            url = entry.get("link", "")
            if not url:
                continue
            items.append({
                "title": entry.get("title", "").strip(),
                "url": url,
                "content": entry.get("summary", ""),
                "author": entry.get("author", ""),
                "image_url": _extract_image(entry),
                "published_at": _parse_date(entry),
                "url_hash": _hash_url(url),
            })
    except Exception as e:
        logger.warning("Feed fetch error for %s: %s", source.name, e)
    return items


def _extract_image(entry) -> str | None:
    """Try to pull a thumbnail/media image from an RSS entry."""
    if hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
        return entry.media_thumbnail[0].get("url")
    if hasattr(entry, "media_content") and entry.media_content:
        return entry.media_content[0].get("url")
    return None


def store_items(db: Session, source: Source, items: list[dict]) -> int:
    """Insert new items; skip duplicates by url_hash. Returns count inserted."""
    inserted = 0
    existing_hashes = {h for (h,) in db.query(NewsItem.url_hash).all()}
    for item in items:
        if item["url_hash"] in existing_hashes:
            continue
        news = NewsItem(source_id=source.id, **item)
        db.add(news)
        inserted += 1
    db.commit()
    return inserted


async def run_ingestion(db: Session):
    """Full ingestion run: fetch all sources, store new items."""
    sources = ensure_sources(db)
    total = 0
    for src in sources.values():
        if not src.active:
            continue
        items = await fetch_feed(src)
        count = store_items(db, src, items)
        src.last_fetched_at = datetime.utcnow()
        db.commit()
        total += count
        logger.info("Fetched %s → %d new items", src.name, count)
    logger.info("Ingestion complete: %d total new items", total)
    return total