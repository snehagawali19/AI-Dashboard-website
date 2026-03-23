from fastapi import APIRouter, Depends, Query, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import get_db
from app.models.models import NewsItem, Favorite
from app.schemas import NewsItemOut, NewsItemDetail, PaginatedNews
from app.services import ai_service
import uuid

router = APIRouter(prefix="/api/news", tags=["news"])

# Demo user_id (replace with real auth in production)
DEMO_USER_ID = "00000000-0000-0000-0000-000000000001"


def _annotate_favorites(items: list[NewsItem], db: Session) -> list[str]:
    fav_ids = {
        str(f.news_item_id)
        for f in db.query(Favorite).filter(
            Favorite.user_id == DEMO_USER_ID
        ).all()
    }
    return fav_ids


@router.get("/", response_model=PaginatedNews)
def list_news(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=50),
    category: str | None = None,
    tag: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(NewsItem).join(NewsItem.source)
    if category:
        from app.models import Source
        query = query.filter(Source.category == category)
    if tag:
        query = query.filter(NewsItem.tags.contains([tag]))

    total = query.count()
    items = (
        query.order_by(desc(NewsItem.published_at))
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )
    fav_ids = _annotate_favorites(items, db)
    out = []
    for item in items:
        d = NewsItemOut.model_validate(item)
        d.is_favorited = str(item.id) in fav_ids
        out.append(d)

    return PaginatedNews(
        items=out, total=total, page=page,
        per_page=per_page, has_more=(page * per_page) < total
    )


@router.get("/{item_id}", response_model=NewsItemDetail)
def get_news_item(item_id: uuid.UUID, db: Session = Depends(get_db)):
    from fastapi import HTTPException
    item = db.query(NewsItem).filter(NewsItem.id == item_id).first()
    if not item:
        raise HTTPException(404, "Not found")
    fav = db.query(Favorite).filter(
        Favorite.user_id == DEMO_USER_ID,
        Favorite.news_item_id == item_id,
    ).first()
    d = NewsItemDetail.model_validate(item)
    d.is_favorited = fav is not None
    return d


@router.post("/{item_id}/process-ai")
async def process_ai(item_id: uuid.UUID, db: Session = Depends(get_db)):
    """Manually trigger AI processing for a single item."""
    from fastapi import HTTPException
    item = db.query(NewsItem).filter(NewsItem.id == item_id).first()
    if not item:
        raise HTTPException(404, "Not found")
    updates = await ai_service.process_news_item(item)
    for k, v in updates.items():
        setattr(item, k, v)
    db.commit()
    return {"status": "ok", "tags": item.tags, "summary": item.summary[:100]}