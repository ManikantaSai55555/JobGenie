from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from app.db.session import get_db
from app.models import JobPosting, User
from app.schemas import JobRead
from app.utils.auth import get_current_user_optional
from app.services.matching import score_jobs_for_user

router = APIRouter()


@router.get("/", response_model=List[JobRead])
def list_jobs(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
    q: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    company: Optional[str] = Query(None),
    job_type: Optional[str] = Query(None),
    min_salary: Optional[int] = Query(None),
    max_experience: Optional[int] = Query(None),
    order_by: str = Query("latest"),  # latest|match|salary
    limit: int = Query(50, ge=1, le=200),
):
    query = db.query(JobPosting)

    if q:
        like = f"%{q.lower()}%"
        query = query.filter(or_(func.lower(JobPosting.title).like(like), func.lower(JobPosting.description).like(like)))
    if location:
        query = query.filter(func.lower(JobPosting.location) == location.lower())

    if company:
        query = query.filter(func.lower(JobPosting.company) == company.lower())
    if job_type:
        query = query.filter(JobPosting.job_type == job_type)
    if min_salary is not None:
        query = query.filter(JobPosting.salary_min >= min_salary)
    if max_experience is not None:
        query = query.filter(JobPosting.experience_max <= max_experience)

    jobs = query.limit(limit).all()

    if current_user:
        scored = score_jobs_for_user(current_user, jobs)
    else:
        scored = [(j, None) for j in jobs]

    if order_by == "match":
        scored.sort(key=lambda x: (x[1] or 0.0), reverse=True)
    elif order_by == "salary":
        scored.sort(key=lambda x: (x[0].salary_max or x[0].salary_min or 0), reverse=True)
    else:  # latest
        scored.sort(key=lambda x: x[0].published_at or x[0].created_at, reverse=True)

    return [JobRead.model_validate({**j.__dict__, "match_score": s}) for j, s in scored]


@router.get("/recommended", response_model=List[JobRead])
def recommended_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional),
    limit: int = Query(50, ge=1, le=200),
):
    jobs = db.query(JobPosting).limit(limit).all()
    if not current_user:
        return [JobRead.model_validate(j) for j in jobs]
    scored = score_jobs_for_user(current_user, jobs)
    scored.sort(key=lambda x: (x[1] or 0.0), reverse=True)
    return [JobRead.model_validate({**j.__dict__, "match_score": s}) for j, s in scored]
