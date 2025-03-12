"""
Admin-related Celery tasks for the LinkedIn AI Agent.
These tasks are typically scheduled to run periodically.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from sqlalchemy import or_

from src.app.db.session import SessionLocal
from src.app.models.user import User
from src.app.models.job import Job
from src.app.models.application import Application, Resume, CoverLetter
from src.app.services.user import get_users
from src.worker.main import celery_app
from src.worker.tasks.linkedin import sync_profile, search_jobs, find_matching_jobs

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, name="admin.sync_all_profiles")
def sync_all_profiles(self) -> Dict[str, Any]:
    """
    Synchronize LinkedIn profiles for all users.
    
    Returns:
        Dict containing the result of the sync operation
    """
    logger.info("Syncing LinkedIn profiles for all users")
    
    db = SessionLocal()
    try:
        # Get all users with LinkedIn connected
        users = db.query(User).filter(User.linkedin_access_token.isnot(None)).all()
        
        logger.info(f"Found {len(users)} users with LinkedIn connected")
        
        # Start sync tasks for each user
        sync_tasks = []
        for user in users:
            task = sync_profile.delay(str(user.id))
            sync_tasks.append({
                "user_id": str(user.id),
                "task_id": task.id
            })
        
        return {
            "status": "success",
            "message": f"Started syncing profiles for {len(sync_tasks)} users",
            "task_count": len(sync_tasks),
            "tasks": sync_tasks
        }
    except Exception as e:
        logger.error(f"Error syncing all profiles: {str(e)}")
        return {
            "status": "error",
            "message": f"Error syncing all profiles: {str(e)}"
        }
    finally:
        db.close()

@celery_app.task(bind=True, name="admin.search_jobs_for_all_users")
def search_jobs_for_all_users(self) -> Dict[str, Any]:
    """
    Search for jobs for all users.
    
    Returns:
        Dict containing the result of the job search
    """
    logger.info("Searching jobs for all users")
    
    db = SessionLocal()
    try:
        # Get all users with LinkedIn connected
        users = db.query(User).filter(User.linkedin_access_token.isnot(None)).all()
        
        logger.info(f"Found {len(users)} users with LinkedIn connected")
        
        # Start job search tasks for each user
        search_tasks = []
        for user in users:
            # Get user's search preferences (could be stored in a separate table)
            preferences = user.preferences if hasattr(user, "preferences") else {}
            
            task = search_jobs.delay(
                str(user.id),
                keywords=preferences.get("job_keywords"),
                location=preferences.get("job_location"),
                job_type=preferences.get("job_type"),
                experience_level=preferences.get("experience_level")
            )
            search_tasks.append({
                "user_id": str(user.id),
                "task_id": task.id
            })
        
        return {
            "status": "success",
            "message": f"Started job search for {len(search_tasks)} users",
            "task_count": len(search_tasks),
            "tasks": search_tasks
        }
    except Exception as e:
        logger.error(f"Error searching jobs for all users: {str(e)}")
        return {
            "status": "error",
            "message": f"Error searching jobs for all users: {str(e)}"
        }
    finally:
        db.close()

@celery_app.task(bind=True, name="admin.find_matching_jobs_for_all_users")
def find_matching_jobs_for_all_users(self) -> Dict[str, Any]:
    """
    Find matching jobs for all users.
    
    Returns:
        Dict containing the result of the matching operation
    """
    logger.info("Finding matching jobs for all users")
    
    db = SessionLocal()
    try:
        # Get all users with profiles
        users = db.query(User).all()
        
        logger.info(f"Found {len(users)} users")
        
        # Start matching tasks for each user
        match_tasks = []
        for user in users:
            task = find_matching_jobs.delay(str(user.id))
            match_tasks.append({
                "user_id": str(user.id),
                "task_id": task.id
            })
        
        return {
            "status": "success",
            "message": f"Started finding matching jobs for {len(match_tasks)} users",
            "task_count": len(match_tasks),
            "tasks": match_tasks
        }
    except Exception as e:
        logger.error(f"Error finding matching jobs for all users: {str(e)}")
        return {
            "status": "error",
            "message": f"Error finding matching jobs for all users: {str(e)}"
        }
    finally:
        db.close()

@celery_app.task(bind=True, name="admin.cleanup_old_data")
def cleanup_old_data(self, days: int = 90) -> Dict[str, Any]:
    """
    Clean up old data from the database.
    
    Args:
        days: Number of days to keep data for
        
    Returns:
        Dict containing the result of the cleanup operation
    """
    logger.info(f"Cleaning up data older than {days} days")
    
    db = SessionLocal()
    try:
        # Calculate cutoff date
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Delete old jobs
        old_jobs = db.query(Job).filter(
            or_(
                Job.created_at < cutoff_date,
                Job.last_updated < cutoff_date
            )
        ).all()
        
        job_ids = [str(job.id) for job in old_jobs]
        
        # Delete old applications
        old_applications = db.query(Application).filter(
            or_(
                Application.created_at < cutoff_date,
                Application.last_updated < cutoff_date
            )
        ).all()
        
        application_ids = [str(app.id) for app in old_applications]
        
        # Delete old resumes
        old_resumes = db.query(Resume).filter(
            Resume.created_at < cutoff_date
        ).all()
        
        resume_ids = [str(resume.id) for resume in old_resumes]
        
        # Delete old cover letters
        old_cover_letters = db.query(CoverLetter).filter(
            CoverLetter.created_at < cutoff_date
        ).all()
        
        cover_letter_ids = [str(cl.id) for cl in old_cover_letters]
        
        # Delete all at once
        for application in old_applications:
            db.delete(application)
        
        for resume in old_resumes:
            db.delete(resume)
        
        for cover_letter in old_cover_letters:
            db.delete(cover_letter)
        
        for job in old_jobs:
            db.delete(job)
        
        db.commit()
        
        return {
            "status": "success",
            "message": f"Cleaned up data older than {days} days",
            "deleted_jobs": len(job_ids),
            "deleted_applications": len(application_ids),
            "deleted_resumes": len(resume_ids),
            "deleted_cover_letters": len(cover_letter_ids)
        }
    except Exception as e:
        logger.error(f"Error cleaning up old data: {str(e)}")
        return {
            "status": "error",
            "message": f"Error cleaning up old data: {str(e)}"
        }
    finally:
        db.close()

@celery_app.task(bind=True, name="admin.generate_activity_report")
def generate_activity_report(self, days: int = 7) -> Dict[str, Any]:
    """
    Generate an activity report for the system.
    
    Args:
        days: Number of days to include in the report
        
    Returns:
        Dict containing the activity report
    """
    logger.info(f"Generating activity report for the last {days} days")
    
    db = SessionLocal()
    try:
        # Calculate cutoff date
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Count recent jobs
        recent_jobs_count = db.query(Job).filter(
            Job.created_at >= cutoff_date
        ).count()
        
        # Count recent applications
        recent_applications_count = db.query(Application).filter(
            Application.created_at >= cutoff_date
        ).count()
        
        # Count recent users
        recent_users_count = db.query(User).filter(
            User.created_at >= cutoff_date
        ).count()
        
        # Count submitted applications
        submitted_applications_count = db.query(Application).filter(
            Application.status == "submitted",
            Application.submitted_at >= cutoff_date
        ).count()
        
        # Count users with LinkedIn connected
        linkedin_users_count = db.query(User).filter(
            User.linkedin_access_token.isnot(None)
        ).count()
        
        return {
            "status": "success",
            "message": f"Generated activity report for the last {days} days",
            "period_days": days,
            "recent_jobs": recent_jobs_count,
            "recent_applications": recent_applications_count,
            "recent_users": recent_users_count,
            "submitted_applications": submitted_applications_count,
            "linkedin_users": linkedin_users_count,
            "generated_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error generating activity report: {str(e)}")
        return {
            "status": "error",
            "message": f"Error generating activity report: {str(e)}"
        }
    finally:
        db.close() 