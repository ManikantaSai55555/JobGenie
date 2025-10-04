from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.aggregator.remoteok import RemoteOKProvider
from app.services.aggregator.ingest import upsert_jobs

router = APIRouter()


@router.post("/aggregate/run")
async def run_aggregate(db: Session = Depends(get_db)):
    provider = RemoteOKProvider()
    jobs = await provider.fetch_recent()
    count = upsert_jobs(db, jobs)
    return {"ingested": count}
