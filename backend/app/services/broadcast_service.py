"""
Mock broadcasting service.
In production: swap with SendGrid, LinkedIn API, WhatsApp Business API.
"""
import uuid
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.models import NewsItem, BroadcastLog

logger = logging.getLogger(__name__)


def _mock_email(item: NewsItem, recipient: str | None) -> dict:
    return {
        "to": recipient or "subscriber@example.com",
        "subject": f"[AI News] {item.title[:80]}",
        "body": item.email_caption or item.summary or item.title,
        "provider": "SendGrid (mock)",
    }

def _mock_linkedin(item: NewsItem) -> dict:
    return {
        "text": item.linkedin_caption or f"📰 {item.title}\n\n{item.url}",
        "url": item.url,
        "provider": "LinkedIn API (mock)",
    }

def _mock_whatsapp(item: NewsItem, recipient: str | None) -> dict:
    return {
        "to": recipient or "+91xxxxxxxxxx",
        "message": f"*{item.title}*\n\n{item.summary or ''}\n\n🔗 {item.url}",
        "provider": "WhatsApp Business API (mock)",
    }


CHANNEL_HANDLERS = {
    "email": _mock_email,
    "linkedin": _mock_linkedin,
    "whatsapp": _mock_whatsapp,
}


def broadcast(
    db: Session,
    news_item_id: str,
    channel: str,
    user_id: str | None = None,
    recipient: str | None = None,
) -> dict:
    item = db.query(NewsItem).filter(NewsItem.id == news_item_id).first()
    if not item:
        raise ValueError("News item not found")

    handler = CHANNEL_HANDLERS.get(channel)
    if not handler:
        raise ValueError(f"Unknown channel: {channel}")

    if channel in ("email", "whatsapp"):
        payload = handler(item, recipient)
    else:
        payload = handler(item)

    log = BroadcastLog(
        id=uuid.uuid4(),
        user_id=user_id,
        news_item_id=item.id,
        channel=channel,
        status="sent",
        payload=payload,
        sent_at=datetime.utcnow(),
    )
    db.add(log)
    db.commit()
    logger.info("Broadcast sent: channel=%s item=%s", channel, news_item_id)

    preview = payload.get("body") or payload.get("text") or payload.get("message", "")
    return {
        "id": str(log.id),
        "channel": channel,
        "status": "sent",
        "message": f"Successfully sent via {channel}",
        "preview": preview[:300],
    }