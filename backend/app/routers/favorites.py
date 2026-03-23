from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Favorite, NewsItem
from app.schemas import FavoriteOut
import uuid

router = APIRouter(prefix="/api/favorites", tags=["favorites"])
DEMO_USER_ID = "00000000-0000-0000-0000-000000000001"


@router.get("/", response_model=list[FavoriteOut])
def list_favorites(db: Session = Depends(get_db)):
    return (
        db.query(Favorite)
        .filter(Favorite.user_id == DEMO_USER_ID)
        .order_by(Favorite.created_at.desc())
        .all()
    )


@router.post("/{news_item_id}", status_code=201)
def add_favorite(news_item_id: uuid.UUID, db: Session = Depends(get_db)):
    item = db.query(NewsItem).filter(NewsItem.id == news_item_id).first()
    if not item:
        raise HTTPException(404, "News item not found")
    existing = db.query(Favorite).filter(
        Favorite.user_id == DEMO_USER_ID,
        Favorite.news_item_id == news_item_id,
    ).first()
    if existing:
        return {"status": "already_favorited"}
    fav = Favorite(user_id=DEMO_USER_ID, news_item_id=news_item_id)
    db.add(fav)
    db.commit()
    return {"status": "favorited", "id": str(fav.id)}


@router.delete("/{news_item_id}", status_code=200)
def remove_favorite(news_item_id: uuid.UUID, db: Session = Depends(get_db)):
    fav = db.query(Favorite).filter(
        Favorite.user_id == DEMO_USER_ID,
        Favorite.news_item_id == news_item_id,
    ).first()
    if not fav:
        raise HTTPException(404, "Not favorited")
    db.delete(fav)
    db.commit()
    return {"status": "unfavorited"}