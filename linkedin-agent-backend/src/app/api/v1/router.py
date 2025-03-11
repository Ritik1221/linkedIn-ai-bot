"""
API router for the LinkedIn AI Agent.
"""

from fastapi import APIRouter

from src.app.api.v1.endpoints import auth, profiles, jobs, applications, networking

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(applications.router, prefix="/applications", tags=["applications"])
api_router.include_router(networking.router, prefix="/networking", tags=["networking"]) 