from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Protocol
from datetime import datetime


@dataclass
class NormalizedJob:
    source: str
    external_id: Optional[str]
    title: str
    company: Optional[str]
    location: Optional[str]
    salary_min: Optional[int]
    salary_max: Optional[int]
    experience_min: Optional[int]
    experience_max: Optional[int]
    job_type: Optional[str]
    description: Optional[str]
    url: str
    published_at: Optional[datetime]


class JobProvider(Protocol):
    name: str

    async def fetch_recent(self) -> List[NormalizedJob]:
        ...
