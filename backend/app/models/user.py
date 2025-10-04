from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text
from typing import List, Optional

from .base import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    password_hash: Mapped[str] = mapped_column(String(512))

    resume_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resume_skills: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of skills list

    saved_jobs: Mapped[List["SavedJob"]] = relationship(back_populates="user")
