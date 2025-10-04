from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime


class JobBase(BaseModel):
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    experience_min: Optional[int] = None
    experience_max: Optional[int] = None
    job_type: Optional[str] = None
    url: str
    source: str
    external_id: Optional[str] = None
    published_at: Optional[datetime] = None


class JobRead(JobBase):
    id: int
    match_score: Optional[float] = None

    class Config:
        from_attributes = True


class SavedJobRead(BaseModel):
    id: int
    status: str
    job: JobRead

    class Config:
        from_attributes = True
