"""
Job application endpoints for the LinkedIn AI Agent.
"""

from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session

from src.app.db.session import get_db
from src.app.models.user import User
from src.app.schemas.application import Application, ApplicationCreate, ApplicationUpdate
from src.app.services.application import (
    create_application, 
    get_application, 
    get_applications_by_user,
    get_applications_by_job,
    update_application,
    delete_application,
    get_application_statistics,
    store_resume,
    store_cover_letter,
    track_application_status,
    get_application_timeline
)
from src.app.services.job import get_job
from src.app.services.user import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[Application])
async def read_applications(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve applications for the current user.
    """
    applications = get_applications_by_user(db, user_id=str(current_user.id), skip=skip, limit=limit)
    return applications


@router.post("/", response_model=Application)
async def create_job_application(
    application_in: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new job application.
    """
    # Check if job exists
    job = get_job(db, job_id=application_in.job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )
    
    # Check if user already applied for this job
    existing_applications = get_applications_by_user(db, user_id=str(current_user.id))
    for app in existing_applications:
        if app.job_id == application_in.job_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already applied for this job",
            )
    
    application = create_application(
        db, application_in=application_in, user_id=str(current_user.id)
    )
    return application


@router.get("/statistics", response_model=Dict[str, Any])
async def get_user_application_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get application statistics for the current user.
    """
    statistics = get_application_statistics(db, user_id=str(current_user.id))
    return statistics


@router.get("/job/{job_id}", response_model=List[Application])
async def read_job_applications(
    job_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve applications for a specific job posting.
    Only accessible by the job poster.
    """
    # Check if job exists and user is the poster
    job = get_job(db, job_id=job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )
    
    if str(job.posted_by) != str(current_user.id) and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    applications = get_applications_by_job(db, job_id=job_id, skip=skip, limit=limit)
    return applications


@router.post("/{application_id}/resume", response_model=Application)
async def upload_resume(
    application_id: str,
    resume_content: str = Form(...),
    resume_file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Upload resume for an application.
    """
    application = get_application(db, application_id=application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )
    
    if str(application.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    # Store resume data
    resume_data = {
        "content": resume_content,
        "filename": resume_file.filename if resume_file else None,
        "content_type": resume_file.content_type if resume_file else None,
    }
    
    updated_application = store_resume(db, application_id=application_id, resume_data=resume_data)
    return updated_application


@router.post("/{application_id}/cover-letter", response_model=Application)
async def upload_cover_letter(
    application_id: str,
    cover_letter_content: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Upload cover letter for an application.
    """
    application = get_application(db, application_id=application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )
    
    if str(application.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    # Store cover letter data
    cover_letter_data = {
        "content": cover_letter_content,
    }
    
    updated_application = store_cover_letter(
        db, application_id=application_id, cover_letter_data=cover_letter_data
    )
    return updated_application


@router.post("/{application_id}/status", response_model=Application)
async def update_status(
    application_id: str,
    status: str = Form(...),
    notes: str = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update the status of an application.
    """
    application = get_application(db, application_id=application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )
    
    # Check if user is the applicant or the job poster
    job = get_job(db, job_id=application.job_id)
    if str(application.user_id) != str(current_user.id) and str(job.posted_by) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    updated_application = track_application_status(
        db, application_id=application_id, new_status=status, notes=notes
    )
    return updated_application


@router.get("/{application_id}/timeline", response_model=List[Dict[str, Any]])
async def get_status_timeline(
    application_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get the timeline of status changes for an application.
    """
    application = get_application(db, application_id=application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )
    
    # Check if user is the applicant or the job poster
    job = get_job(db, job_id=application.job_id)
    if str(application.user_id) != str(current_user.id) and str(job.posted_by) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    timeline = get_application_timeline(db, application_id=application_id)
    return timeline


@router.get("/{application_id}", response_model=Application)
async def read_application(
    application_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get application by ID.
    """
    application = get_application(db, application_id=application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )
    
    # Check if user is the applicant or the job poster
    job = get_job(db, job_id=application.job_id)
    if str(application.user_id) != str(current_user.id) and str(job.posted_by) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    return application


@router.put("/{application_id}", response_model=Application)
async def update_application_details(
    application_id: str,
    application_in: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update application details.
    Applicant can update their own application details.
    Job poster can update the status.
    """
    application = get_application(db, application_id=application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )
    
    # Check permissions based on what's being updated
    is_applicant = str(application.user_id) == str(current_user.id)
    job = get_job(db, job_id=application.job_id)
    is_job_poster = str(job.posted_by) == str(current_user.id)
    
    # Only job poster can update status
    if "status" in application_in.model_dump(exclude_unset=True) and not is_job_poster:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the job poster can update the application status",
        )
    
    # Only applicant can update other fields
    if not is_applicant and not is_job_poster:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    application = update_application(db, application=application, application_in=application_in)
    return application


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job_application(
    application_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete an application.
    Only the applicant can delete their application.
    """
    application = get_application(db, application_id=application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )
    
    if str(application.user_id) != str(current_user.id) and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    delete_application(db, application_id=application_id)
    return None 