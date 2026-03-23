import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import news, favorites, broadcast
from app.tasks.scheduler import start_scheduler

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    start_scheduler()
    yield
    # Shutdown: scheduler stops automatically


app = FastAPI(
    title="AI News Dashboard API",
    version="1.0.0",
    description="Aggregate, summarise, and broadcast AI news.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(news.router)
app.include_router(favorites.router)
app.include_router(broadcast.router)


@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}


@app.post("/api/ingest", tags=["admin"])
async def trigger_ingestion():
    """Manually trigger ingestion (useful for demos)."""
    from app.database import SessionLocal
    from app.services.ingestion import run_ingestion
    db = SessionLocal()
    try:
        count = await run_ingestion(db)
        return {"status": "ok", "new_items": count}
    finally:
        db.close()