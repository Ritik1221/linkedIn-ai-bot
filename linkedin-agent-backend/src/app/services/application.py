"""
Application service for the LinkedIn AI Agent.
This module provides functions for job application management, tracking, and document handling.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.app.models.application import Application
from src.app.models.job import Job
from src.app.models.user import User
from src.app.schemas.application import ApplicationCreate, ApplicationUpdate


def get_application(db: Session, application_id: str) -> Optional[Application]:
    """
    Get an application by ID.
    
    Args:
        db: Database session
        application_id: Application ID
        
    Returns:
        Application object if found, None otherwise
    """
    return db.query(Application).filter(Application.id == application_id).first()


def get_applications_by_user(
    db: Session, user_id: str, skip: int = 0, limit: int = 100
) -> List[Application]:
    """
    Get applications by user ID with pagination.
    
    Args:
        db: Database session
        user_id: User ID
        skip: Number of applications to skip
        limit: Maximum number of applications to return
        
    Returns:
        List of application objects
    """
    return (
        db.query(Application)
        .filter(Application.user_id == user_id)
        .order_by(desc(Application.applied_at))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_applications_by_job(
    db: Session, job_id: str, skip: int = 0, limit: int = 100
) -> List[Application]:
    """
    Get applications by job ID with pagination.
    
    Args:
        db: Database session
        job_id: Job ID
        skip: Number of applications to skip
        limit: Maximum number of applications to return
        
    Returns:
        List of application objects
    """
    return (
        db.query(Application)
        .filter(Application.job_id == job_id)
        .order_by(desc(Application.applied_at))
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_application(
    db: Session, application_in: ApplicationCreate, user_id: str
) -> Application:
    """
    Create a new application.
    
    Args:
        db: Database session
        application_in: Application creation data
        user_id: User ID
        
    Returns:
        Created application object
    """
    application_data = application_in.model_dump()
    application_data["user_id"] = user_id
    application_data["applied_at"] = datetime.utcnow()
    application_data["status"] = application_data.get("status", "applied")
    
    db_application = Application(**application_data)
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application


def update_application(
    db: Session, application: Application, application_in: Union[ApplicationUpdate, Dict[str, Any]]
) -> Application:
    """
    Update an application.
    
    Args:
        db: Database session
        application: Application object to update
        application_in: Application update data
        
    Returns:
        Updated application object
    """
    application_data = application.__dict__
    if isinstance(application_in, dict):
        update_data = application_in
    else:
        update_data = application_in.model_dump(exclude_unset=True)
    
    # If status is changing, update the status_updated_at field
    if "status" in update_data and update_data["status"] != application.status:
        update_data["status_updated_at"] = datetime.utcnow()
    
    for field in application_data:
        if field in update_data:
            setattr(application, field, update_data[field])
    
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


def delete_application(db: Session, application_id: str) -> Application:
    """
    Delete an application.
    
    Args:
        db: Database session
        application_id: Application ID
        
    Returns:
        Deleted application object
    """
    application = db.query(Application).filter(Application.id == application_id).first()
    db.delete(application)
    db.commit()
    return application


def get_application_statistics(db: Session, user_id: str) -> Dict[str, Any]:
    """
    Get application statistics for a user.
    
    Args:
        db: Database session
        user_id: User ID
        
    Returns:
        Dictionary with application statistics
    """
    # Get all applications for the user
    applications = db.query(Application).filter(Application.user_id == user_id).all()
    
    # Count applications by status
    status_counts = {}
    for app in applications:
        status = app.status
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Calculate response rate
    total_applications = len(applications)
    responses = sum(
        status_counts.get(status, 0) 
        for status in ["interview", "offer", "rejected"]
    )
    response_rate = (responses / total_applications) * 100 if total_applications > 0 else 0
    
    # Calculate success rate (interviews and offers)
    successes = sum(
        status_counts.get(status, 0) 
        for status in ["interview", "offer"]
    )
    success_rate = (successes / total_applications) * 100 if total_applications > 0 else 0
    
    # Calculate offer rate
    offers = status_counts.get("offer", 0)
    offer_rate = (offers / total_applications) * 100 if total_applications > 0 else 0
    
    # Get applications by month
    applications_by_month = {}
    for app in applications:
        month_key = app.applied_at.strftime("%Y-%m")
        applications_by_month[month_key] = applications_by_month.get(month_key, 0) + 1
    
    return {
        "total_applications": total_applications,
        "status_counts": status_counts,
        "response_rate": response_rate,
        "success_rate": success_rate,
        "offer_rate": offer_rate,
        "applications_by_month": applications_by_month,
    }


def store_resume(db: Session, application_id: str, resume_data: Dict[str, Any]) -> Application:
    """
    Store resume data for an application.
    
    Args:
        db: Database session
        application_id: Application ID
        resume_data: Resume data (content, file path, etc.)
        
    Returns:
        Updated application object
    """
    application = get_application(db, application_id=application_id)
    if not application:
        return None
    
    # Update the resume field
    application = update_application(
        db, 
        application=application, 
        application_in={"resume": resume_data}
    )
    
    return application


def store_cover_letter(db: Session, application_id: str, cover_letter_data: Dict[str, Any]) -> Application:
    """
    Store cover letter data for an application.
    
    Args:
        db: Database session
        application_id: Application ID
        cover_letter_data: Cover letter data (content, file path, etc.)
        
    Returns:
        Updated application object
    """
    application = get_application(db, application_id=application_id)
    if not application:
        return None
    
    # Update the cover_letter field
    application = update_application(
        db, 
        application=application, 
        application_in={"cover_letter": cover_letter_data}
    )
    
    return application


def track_application_status(db: Session, application_id: str, new_status: str, notes: Optional[str] = None) -> Application:
    """
    Update the status of an application and add tracking notes.
    
    Args:
        db: Database session
        application_id: Application ID
        new_status: New application status
        notes: Optional notes about the status change
        
    Returns:
        Updated application object
    """
    application = get_application(db, application_id=application_id)
    if not application:
        return None
    
    # Create status history entry
    status_history = application.status_history or []
    status_history.append({
        "status": application.status,
        "changed_at": application.status_updated_at.isoformat() if application.status_updated_at else datetime.utcnow().isoformat(),
        "notes": notes
    })
    
    # Update application status
    application = update_application(
        db, 
        application=application, 
        application_in={
            "status": new_status,
            "status_history": status_history,
            "notes": notes if notes else application.notes
        }
    )
    
    return application


def get_application_timeline(db: Session, application_id: str) -> List[Dict[str, Any]]:
    """
    Get the timeline of an application's status changes.
    
    Args:
        db: Database session
        application_id: Application ID
        
    Returns:
        List of status change events
    """
    application = get_application(db, application_id=application_id)
    if not application or not application.status_history:
        return []
    
    # Add the current status to the timeline
    timeline = application.status_history.copy()
    timeline.append({
        "status": application.status,
        "changed_at": application.status_updated_at.isoformat() if application.status_updated_at else datetime.utcnow().isoformat(),
        "notes": application.notes
    })
    
    # Sort by changed_at date
    timeline.sort(key=lambda x: x["changed_at"])
    
    return timeline 