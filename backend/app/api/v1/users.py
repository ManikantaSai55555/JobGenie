from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import User
from app.schemas import UserRead, ResumeUpdate
from app.utils.resume_parser import extract_text_from_file, extract_skills_simple
from app.utils.auth import get_current_user

router = APIRouter()


@router.get("/me", response_model=UserRead)
def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/me/resume", response_model=UserRead)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    text = await extract_text_from_file(file)
    skills = extract_skills_simple(text)
    current_user.resume_text = text
    current_user.resume_skills = __import__("json").dumps(skills)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.put("/me/resume", response_model=UserRead)
async def set_resume(
    payload: ResumeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if payload.resume_text is not None:
        current_user.resume_text = payload.resume_text
    if payload.resume_skills is not None:
        current_user.resume_skills = __import__("json").dumps(payload.resume_skills)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user
