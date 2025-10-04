from __future__ import annotations
from typing import List
from sqlalchemy.orm import Session
import asyncio

from app.core.config import settings
from .remoteok import RemoteOKProvider
from .ingest import upsert_jobs


async def run_all_providers_async(db: Session) -> int:
    # For now only RemoteOK; can be extended via settings.aggregation_providers
    providers = []
    if "remoteok" in settings.aggregation_providers:
        providers.append(RemoteOKProvider())

    total = 0
    for p in providers:
        jobs = await p.fetch_recent()
        total += upsert_jobs(db, jobs)
    return total
