from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Enum, Integer, DateTime, ForeignKey, UniqueConstraint, Index
from datetime import datetime
from typing import Optional, List

from .base import Base, TimestampMixin


class JobTypeEnum(str):
    FULL_TIME = "full_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    PART_TIME = "part_time"
    TEMPORARY = "temporary"
    OTHER = "other"


class JobPosting(Base, TimestampMixin):
    __tablename__ = "job_postings"
    __table_args__ = (
        UniqueConstraint("source", "external_id", name="uq_source_external_id"),
        Index("ix_title_company_url", "title", "company", "url"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String(50))
    external_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    title: Mapped[str] = mapped_column(String(255), index=True)
    company: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)

    salary_min: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    experience_min: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    experience_max: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    job_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # from JobTypeEnum

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    url: Mapped[str] = mapped_column(String(2048))
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    saved_by_users: Mapped[List["SavedJob"]] = relationship(back_populates="job")


class SavedJob(Base, TimestampMixin):
    __tablename__ = "saved_jobs"
    __table_args__ = (
        UniqueConstraint("user_id", "job_id", name="uq_user_job"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    job_id: Mapped[int] = mapped_column(ForeignKey("job_postings.id", ondelete="CASCADE"))

    status: Mapped[str] = mapped_column(String(50), default="saved")  # saved|applied|shortlisted|interview

    user: Mapped["User"] = relationship(back_populates="saved_jobs")
    job: Mapped["JobPosting"] = relationship(back_populates="saved_by_users")
