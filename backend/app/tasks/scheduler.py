import logging
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.config import settings
from app.database import SessionLocal
from app.services.ingestion import run_ingestion
from app.services.ai_service import process_news_item
from app.models import NewsItem

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()


def _run_ingestion_sync():
    db = SessionLocal()
    try:
        asyncio.run(run_ingestion(db))
    except Exception as e:
        logger.error("Ingestion job failed: %s", e)
    finally:
        db.close()


def _run_ai_processing():
    """Process up to 10 unprocessed items per run (rate-limit-safe)."""
    db = SessionLocal()
    try:
        items = (
            db.query(NewsItem)
            .filter(NewsItem.ai_processed == False)
            .limit(10)
            .all()
        )
        for item in items:
            updates = asyncio.run(process_news_item(item))
            for k, v in updates.items():
                setattr(item, k, v)
            db.commit()
            logger.info("AI processed: %s", item.title[:60])
    except Exception as e:
        logger.error("AI processing job failed: %s", e)
    finally:
        db.close()


def start_scheduler():
    scheduler.add_job(
        _run_ingestion_sync,
        IntervalTrigger(minutes=settings.FETCH_INTERVAL_MINUTES),
        id="ingestion", replace_existing=True,
    )
    scheduler.add_job(
        _run_ai_processing,
        IntervalTrigger(minutes=5),
        id="ai_processing", replace_existing=True,
    )
    scheduler.start()
    logger.info("Scheduler started (ingestion every %d min)", settings.FETCH_INTERVAL_MINUTES)