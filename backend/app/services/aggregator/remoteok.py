from __future__ import annotations
from typing import List, Optional
from datetime import datetime, timezone
import httpx

from .base import NormalizedJob, JobProvider


class RemoteOKProvider:
    name = "remoteok"
    API_URL = "https://remoteok.com/api"

    async def fetch_recent(self) -> List[NormalizedJob]:
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.get(self.API_URL, headers={"Accept": "application/json"})
            resp.raise_for_status()
            data = resp.json()
        jobs: List[NormalizedJob] = []
        for item in data:
            if not isinstance(item, dict):
                continue
            if item.get("position") is None and item.get("role") is None:
                # Skip metadata rows
                continue
            title = item.get("position") or item.get("role") or ""
            company = item.get("company")
            location = item.get("location") or item.get("candidate_required_location")
            url = item.get("url") or item.get("apply_url") or item.get("url") or ""
            description = item.get("description") or item.get("tags")
            published_str = item.get("date") or item.get("published_at")
            published_at = None
            if published_str:
                try:
                    published_at = datetime.fromisoformat(published_str.replace("Z", "+00:00")).astimezone(timezone.utc)
                except Exception:
                    published_at = None
            external_id = str(item.get("id") or "") or None
            jobs.append(
                NormalizedJob(
                    source=self.name,
                    external_id=external_id,
                    title=title,
                    company=company,
                    location=location,
                    salary_min=None,
                    salary_max=None,
                    experience_min=None,
                    experience_max=None,
                    job_type="remote",
                    description=str(description) if description is not None else None,
                    url=url,
                    published_at=published_at,
                )
            )
        return jobs
