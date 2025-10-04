from fastapi import APIRouter
from . import users, auth, jobs, saved, admin

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(saved.router, prefix="/saved", tags=["saved"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])