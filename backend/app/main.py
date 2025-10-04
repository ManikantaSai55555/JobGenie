from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import engine
from app.models.base import Base

from app.api.v1.router import api_router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.aggregator.runner import run_all_providers_async
import asyncio

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    # Ensure DB tables exist
    Base.metadata.create_all(bind=engine)
    # Schedule daily aggregation at 02:00 UTC
    scheduler = AsyncIOScheduler()

    async def _task_async():
        db: Session = SessionLocal()
        try:
            await run_all_providers_async(db)
        finally:
            db.close()

    scheduler.add_job(lambda: asyncio.create_task(_task_async()), CronTrigger(hour=2, minute=0))
    scheduler.start()


app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
