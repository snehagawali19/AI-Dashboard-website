from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import BroadcastRequest, BroadcastResponse
from app.services.broadcast_service import broadcast
from app.models.models import BroadcastLog

router = APIRouter(prefix="/api/broadcast", tags=["broadcast"])
DEMO_USER_ID = "00000000-0000-0000-0000-000000000001"

VALID_CHANNELS = {"email", "linkedin", "whatsapp"}


@router.post("/", response_model=BroadcastResponse)
def send_broadcast(req: BroadcastRequest, db: Session = Depends(get_db)):
    if req.channel not in VALID_CHANNELS:
        raise HTTPException(400, f"Invalid channel. Use: {VALID_CHANNELS}")
    try:
        result = broadcast(
            db=db,
            news_item_id=str(req.news_item_id),
            channel=req.channel,
            user_id=DEMO_USER_ID,
            recipient=req.recipient,
        )
        return BroadcastResponse(**result)
    except ValueError as e:
        raise HTTPException(400, str(e))