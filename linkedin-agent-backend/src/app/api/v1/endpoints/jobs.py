"""
Job endpoints for the LinkedIn AI Agent.
"""

from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.app.db.session import get_db
from src.app.models.user import User
from src.app.schemas.job import Job, JobCreate, JobUpdate
from src.app.services.job import (
    create_job, 
    get_job, 
    get_jobs, 
    update_job, 
    delete_job, 
    search_jobs,
    recommend_jobs_for_profile,
    get_trending_jobs
)
from src.app.services.profile import get_profile_by_user_id
from src.app.services.user import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[Job])
async def read_jobs(
    skip: int = 0,
    limit: int = 100,
    query: Optional[str] = None,
    location: Optional[str] = None,
    company: Optional[str] = None,
    job_type: Optional[str] = None,
    experience_level: Optional[str] = None,
    posted_within_days: Optional[int] = None,
    skills: Optional[List[str]] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve jobs with optional filtering.
    """
    jobs = search_jobs(
        db, 
        query=query,
        location=location,
        company=company,
        job_type=job_type,
        experience_level=experience_level,
        posted_within_days=posted_within_days,
        skills=skills,
        skip=skip, 
        limit=limit
    )
    return jobs


@router.post("/", response_model=Job)
async def create_new_job(
    job_in: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new job posting.
    """
    # Set the posted_by field to the current user's ID
    job_data = job_in.model_dump()
    job_data["posted_by"] = str(current_user.id)
    
    job = create_job(db, JobCreate(**job_data))
    return job


@router.get("/my-postings", response_model=List[Job])
async def read_user_jobs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get jobs posted by current user.
    """
    # Filter jobs by the current user's ID
    jobs = search_jobs(
        db,
        skip=skip,
        limit=limit,
        posted_by=str(current_user.id)
    )
    return jobs


@router.get("/recommendations", response_model=List[dict])
async def get_job_recommendations(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get job recommendations based on user profile.
    """
    profile = get_profile_by_user_id(db, user_id=str(current_user.id))
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Please create a profile first to get job recommendations.",
        )
    
    recommendations = recommend_jobs_for_profile(db, profile=profile, limit=limit)
    return recommendations


@router.get("/trending", response_model=List[Job])
async def get_trending_job_listings(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get trending job listings.
    """
    trending = get_trending_jobs(db, limit=limit)
    return trending


@router.get("/{job_id}", response_model=Job)
async def read_job(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get job by ID.
    """
    job = get_job(db, job_id=job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )
    return job


@router.put("/{job_id}", response_model=Job)
async def update_job_posting(
    job_id: str,
    job_in: JobUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update job posting.
    """
    job = get_job(db, job_id=job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )
    
    # Check if the current user is the one who posted the job
    if str(job.posted_by) != str(current_user.id) and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    job = update_job(db, job=job, job_in=job_in)
    return job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job_posting(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete job posting.
    """
    job = get_job(db, job_id=job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )
    
    # Check if the current user is the one who posted the job
    if str(job.posted_by) != str(current_user.id) and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    delete_job(db, job_id=job_id)
    return None 