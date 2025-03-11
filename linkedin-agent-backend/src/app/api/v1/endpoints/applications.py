"""
Job application endpoints for the LinkedIn AI Agent.
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.app.db.session import get_db
from src.app.schemas.application import Application, ApplicationCreate, ApplicationUpdate
# from src.app.services.application import create_application, get_application, get_applications, update_application
# from src.app.services.user import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[Application])
async def read_applications(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve applications for the current user.
    """
    # Uncomment when application service is implemented
    # applications = get_applications_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    
    # For now, return a placeholder list of applications
    return [
        {
            "id": "00000000-0000-0000-0000-000000000000",
            "job_id": "00000000-0000-0000-0000-000000000000",
            "user_id": "00000000-0000-0000-0000-000000000000",
            "cover_letter": "I am excited to apply for this position...",
            "resume_url": "https://example.com/resume.pdf",
            "status": "pending",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00",
        }
    ]


@router.post("/", response_model=Application)
async def create_job_application(
    application_in: ApplicationCreate,
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_active_user),
) -> Any:
    """
    Create new job application.
    """
    # Uncomment when application service is implemented
    # # Check if job exists
    # job = get_job(db, id=application_in.job_id)
    # if not job:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Job not found",
    #     )
    # # Check if user already applied for this job
    # existing_application = get_application_by_job_and_user(
    #     db, job_id=application_in.job_id, user_id=current_user.id
    # )
    # if existing_application:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="You have already applied for this job",
    #     )
    # application = create_application(
    #     db, application_in=application_in, user_id=current_user.id
    # )
    
    # For now, return a placeholder application
    return {
        "id": "00000000-0000-0000-0000-000000000000",
        "job_id": application_in.job_id,
        "user_id": "00000000-0000-0000-0000-000000000000",
        "cover_letter": application_in.cover_letter,
        "resume_url": application_in.resume_url,
        "status": "pending",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00",
    }


@router.get("/job/{job_id}", response_model=List[Application])
async def read_job_applications(
    job_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve applications for a specific job posting.
    Only accessible by the job poster.
    """
    # Uncomment when application service is implemented
    # # Check if job exists and user is the poster
    # job = get_job(db, id=job_id)
    # if not job:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Job not found",
    #     )
    # if job.posted_by != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Not enough permissions",
    #     )
    # applications = get_applications_by_job(db, job_id=job_id, skip=skip, limit=limit)
    
    # For now, return a placeholder list of applications
    return [
        {
            "id": "00000000-0000-0000-0000-000000000000",
            "job_id": job_id,
            "user_id": "00000000-0000-0000-0000-000000000000",
            "cover_letter": "I am excited to apply for this position...",
            "resume_url": "https://example.com/resume.pdf",
            "status": "pending",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00",
        }
    ]


@router.get("/{application_id}", response_model=Application)
async def read_application(
    application_id: str,
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_active_user),
) -> Any:
    """
    Get application by ID.
    """
    # Uncomment when application service is implemented
    # application = get_application(db, id=application_id)
    # if not application:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Application not found",
    #     )
    # # Check if user is the applicant or the job poster
    # if application.user_id != current_user.id:
    #     job = get_job(db, id=application.job_id)
    #     if job.posted_by != current_user.id:
    #         raise HTTPException(
    #             status_code=status.HTTP_403_FORBIDDEN,
    #             detail="Not enough permissions",
    #         )
    
    # For now, return a placeholder application
    return {
        "id": application_id,
        "job_id": "00000000-0000-0000-0000-000000000000",
        "user_id": "00000000-0000-0000-0000-000000000000",
        "cover_letter": "I am excited to apply for this position...",
        "resume_url": "https://example.com/resume.pdf",
        "status": "pending",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00",
    }


@router.put("/{application_id}", response_model=Application)
async def update_application_status(
    application_id: str,
    application_in: ApplicationUpdate,
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_active_user),
) -> Any:
    """
    Update application status.
    Only the job poster can update the status.
    """
    # Uncomment when application service is implemented
    # application = get_application(db, id=application_id)
    # if not application:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Application not found",
    #     )
    # # Check if user is the job poster
    # job = get_job(db, id=application.job_id)
    # if job.posted_by != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Not enough permissions",
    #     )
    # application = update_application(db, application=application, application_in=application_in)
    
    # For now, return a placeholder updated application
    return {
        "id": application_id,
        "job_id": "00000000-0000-0000-0000-000000000000",
        "user_id": "00000000-0000-0000-0000-000000000000",
        "cover_letter": "I am excited to apply for this position...",
        "resume_url": "https://example.com/resume.pdf",
        "status": application_in.status or "pending",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00",
    } 