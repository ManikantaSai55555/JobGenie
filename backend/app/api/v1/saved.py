from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import SavedJob, JobPosting, User
from app.schemas import SavedJobRead
from app.utils.auth import get_current_user

router = APIRouter()


@router.get("/", response_model=List[SavedJobRead])
def list_saved(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    items = db.query(SavedJob).filter(SavedJob.user_id == current_user.id).all()
    return items


@router.post("/{job_id}", response_model=SavedJobRead)
def save_job(job_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    existing = db.query(SavedJob).filter(SavedJob.user_id == current_user.id, SavedJob.job_id == job_id).first()
    if existing:
        return existing
    item = SavedJob(user_id=current_user.id, job_id=job_id, status="saved")
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{saved_id}/{status}", response_model=SavedJobRead)
def update_status(saved_id: int, status: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = db.query(SavedJob).filter(SavedJob.id == saved_id, SavedJob.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Saved item not found")
    item.status = status
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
