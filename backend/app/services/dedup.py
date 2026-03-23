"""
Two-layer deduplication:
  1. URL hash (fast, exact)
  2. Cosine similarity on embeddings (semantic, catches reposts)
"""
import numpy as np
from sqlalchemy.orm import Session
from app.models import NewsItem

COSINE_THRESHOLD = 0.92  # above this = duplicate


def cosine_similarity(a: list[float], b: list[float]) -> float:
    a, b = np.array(a), np.array(b)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    return float(np.dot(a, b) / denom) if denom else 0.0


def is_semantic_duplicate(
    db: Session,
    embedding: list[float],
    exclude_id: str | None = None,
) -> bool:
    """Check if any existing item is semantically similar to this embedding."""
    if not embedding:
        return False

    query = db.query(NewsItem.id, NewsItem.embedding).filter(
        NewsItem.embedding.isnot(None)
    )
    if exclude_id:
        query = query.filter(NewsItem.id != exclude_id)

    for item_id, stored_emb in query.all():
        if stored_emb and cosine_similarity(embedding, stored_emb) >= COSINE_THRESHOLD:
            return True
    return False