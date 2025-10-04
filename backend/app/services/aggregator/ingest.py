from __future__ import annotations
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timedelta, timezone

from app.core.config import settings
from app.models import JobPosting
from .base import NormalizedJob


def upsert_jobs(db: Session, jobs: List[NormalizedJob]) -> int:
    inserted_or_updated = 0
    for j in jobs:
        # Deduplicate by source+external_id, or by title+company+url
        existing = None
        if j.external_id:
            existing = db.execute(
                select(JobPosting).where(JobPosting.source == j.source, JobPosting.external_id == j.external_id)
            ).scalars().first()
        if not existing:
            existing = db.execute(
                select(JobPosting).where(
                    JobPosting.title == j.title,
                    JobPosting.company == j.company,
                    JobPosting.url == j.url,
                )
            ).scalars().first()
        if existing:
            # Update minimal fields that may change
            existing.location = j.location
            existing.salary_min = j.salary_min
            existing.salary_max = j.salary_max
            existing.experience_min = j.experience_min
            existing.experience_max = j.experience_max
            existing.job_type = j.job_type
            existing.description = j.description
            existing.published_at = j.published_at
            db.add(existing)
            inserted_or_updated += 1
        else:
            row = JobPosting(
                source=j.source,
                external_id=j.external_id,
                title=j.title,
                company=j.company,
                location=j.location,
                salary_min=j.salary_min,
                salary_max=j.salary_max,
                experience_min=j.experience_min,
                experience_max=j.experience_max,
                job_type=j.job_type,
                description=j.description,
                url=j.url,
                published_at=j.published_at,
            )
            db.add(row)
            inserted_or_updated += 1
    db.commit()
    return inserted_or_updated
