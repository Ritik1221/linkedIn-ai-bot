"""
LinkedIn-related Celery tasks for the LinkedIn AI Agent.
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

from sqlalchemy.orm import Session

from src.app.core.linkedin_client import LinkedInClient, get_linkedin_client
from src.app.db.session import SessionLocal
from src.app.models.user import User
from src.app.models.profile import Profile, Experience, Education, Certification, Skill
from src.app.models.job import Job
from src.app.services.user import get_user, update_user
from src.app.services.profile import create_profile, update_profile, get_profile_by_user
from src.app.services.job import create_job, update_job, get_job_by_linkedin_id
from src.worker.main import celery_app

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, name="linkedin.sync_profile")
def sync_profile(self, user_id: str) -> Dict[str, Any]:
    """
    Synchronize a user's LinkedIn profile data.
    
    Args:
        user_id: The ID of the user whose profile to sync
        
    Returns:
        Dict containing the result of the sync operation
    """
    logger.info(f"Syncing LinkedIn profile for user {user_id}")
    
    db = SessionLocal()
    try:
        # Get user
        user = get_user(db, user_id=user_id)
        if not user or not user.linkedin_access_token:
            return {
                "status": "error",
                "user_id": user_id,
                "message": "User not found or LinkedIn not connected"
            }
        
        # Check if token is expired and refresh if needed
        now = datetime.utcnow().timestamp()
        if user.linkedin_token_expires_at and user.linkedin_token_expires_at.timestamp() < now:
            if not user.linkedin_refresh_token:
                return {
                    "status": "error",
                    "user_id": user_id,
                    "message": "LinkedIn token expired and no refresh token available"
                }
            
            # Refresh token
            linkedin_client = get_linkedin_client()
            try:
                token_data = linkedin_client.refresh_access_token(user.linkedin_refresh_token)
                
                # Update user with new token
                update_user(db, user=user, user_in={
                    "linkedin_access_token": token_data.get("access_token"),
                    "linkedin_refresh_token": token_data.get("refresh_token", user.linkedin_refresh_token),
                    "linkedin_token_expires_at": datetime.fromtimestamp(token_data.get("expires_at", 0))
                })
            except Exception as e:
                logger.error(f"Failed to refresh LinkedIn token: {str(e)}")
                return {
                    "status": "error",
                    "user_id": user_id,
                    "message": f"Failed to refresh LinkedIn token: {str(e)}"
                }
        
        # Get LinkedIn profile data
        linkedin_client = get_linkedin_client()
        try:
            profile_data = linkedin_client.get_profile(user.linkedin_access_token)
        except Exception as e:
            logger.error(f"Failed to get LinkedIn profile: {str(e)}")
            return {
                "status": "error",
                "user_id": user_id,
                "message": f"Failed to get LinkedIn profile: {str(e)}"
            }
        
        # Update user profile
        existing_profile = get_profile_by_user(db, user_id=user_id)
        
        profile_update = {
            "linkedin_profile_id": profile_data.get("id"),
            "headline": profile_data.get("headline", ""),
            "summary": profile_data.get("summary", ""),
            "industry": profile_data.get("industry", ""),
            "location": profile_data.get("location", {}).get("name", ""),
            "profile_picture_url": profile_data.get("profilePicture", ""),
            "public_profile_url": profile_data.get("publicProfileUrl", ""),
            "last_updated": datetime.utcnow()
        }
        
        if existing_profile:
            profile = update_profile(db, profile=existing_profile, profile_in=profile_update)
        else:
            profile_update["user_id"] = user_id
            profile = create_profile(db, profile_in=profile_update)
        
        # TODO: Sync experiences, education, certifications, and skills
        # This would require additional API calls to LinkedIn
        
        return {
            "status": "success",
            "user_id": user_id,
            "message": "Profile synced successfully",
            "profile_id": str(profile.id)
        }
    except Exception as e:
        logger.error(f"Error syncing LinkedIn profile: {str(e)}")
        return {
            "status": "error",
            "user_id": user_id,
            "message": f"Error syncing LinkedIn profile: {str(e)}"
        }
    finally:
        db.close()


@celery_app.task(bind=True, name="linkedin.search_jobs")
def search_jobs(
    self, 
    user_id: str, 
    keywords: Optional[str] = None,
    location: Optional[str] = None,
    job_type: Optional[str] = None,
    experience_level: Optional[str] = None,
    limit: int = 20
) -> Dict[str, Any]:
    """
    Search for jobs on LinkedIn based on criteria.
    
    Args:
        user_id: The ID of the user performing the search
        keywords: Job keywords to search for
        location: Location to search in
        job_type: Type of job (full-time, part-time, etc.)
        experience_level: Experience level required
        limit: Maximum number of results to return
        
    Returns:
        Dict containing the search results
    """
    logger.info(f"Searching LinkedIn jobs for user {user_id}")
    
    db = SessionLocal()
    try:
        # Get user
        user = get_user(db, user_id=user_id)
        if not user or not user.linkedin_access_token:
            return {
                "status": "error",
                "user_id": user_id,
                "message": "User not found or LinkedIn not connected"
            }
        
        # Check if token is expired and refresh if needed
        now = datetime.utcnow().timestamp()
        if user.linkedin_token_expires_at and user.linkedin_token_expires_at.timestamp() < now:
            if not user.linkedin_refresh_token:
                return {
                    "status": "error",
                    "user_id": user_id,
                    "message": "LinkedIn token expired and no refresh token available"
                }
            
            # Refresh token
            linkedin_client = get_linkedin_client()
            try:
                token_data = linkedin_client.refresh_access_token(user.linkedin_refresh_token)
                
                # Update user with new token
                update_user(db, user=user, user_in={
                    "linkedin_access_token": token_data.get("access_token"),
                    "linkedin_refresh_token": token_data.get("refresh_token", user.linkedin_refresh_token),
                    "linkedin_token_expires_at": datetime.fromtimestamp(token_data.get("expires_at", 0))
                })
            except Exception as e:
                logger.error(f"Failed to refresh LinkedIn token: {str(e)}")
                return {
                    "status": "error",
                    "user_id": user_id,
                    "message": f"Failed to refresh LinkedIn token: {str(e)}"
                }
        
        # Search for jobs
        linkedin_client = get_linkedin_client()
        try:
            jobs = linkedin_client.search_jobs(
                access_token=user.linkedin_access_token,
                keywords=keywords,
                location=location,
                job_type=job_type,
                experience_level=experience_level,
                limit=limit
            )
        except Exception as e:
            logger.error(f"Failed to search LinkedIn jobs: {str(e)}")
            return {
                "status": "error",
                "user_id": user_id,
                "message": f"Failed to search LinkedIn jobs: {str(e)}"
            }
        
        # Store jobs in database
        stored_jobs = []
        for job_data in jobs:
            linkedin_job_id = job_data.get("id")
            if not linkedin_job_id:
                continue
            
            # Check if job already exists
            existing_job = get_job_by_linkedin_id(db, linkedin_job_id=linkedin_job_id)
            
            job_update = {
                "title": job_data.get("title", ""),
                "company": job_data.get("company", ""),
                "location": job_data.get("location", ""),
                "description": job_data.get("description", ""),
                "apply_url": job_data.get("apply_url", ""),
                "linkedin_job_id": linkedin_job_id,
                "company_linkedin_id": job_data.get("company_id", ""),
                "job_type": job_type,
                "experience_level": experience_level,
                "last_updated": datetime.utcnow()
            }
            
            if existing_job:
                job = update_job(db, job=existing_job, job_in=job_update)
            else:
                job_update["posted_by"] = None  # Not posted by a user
                job = create_job(db, job_in=job_update)
            
            stored_jobs.append(str(job.id))
        
        return {
            "status": "success",
            "user_id": user_id,
            "message": f"Found {len(jobs)} jobs",
            "job_count": len(jobs),
            "stored_job_count": len(stored_jobs),
            "job_ids": stored_jobs
        }
    except Exception as e:
        logger.error(f"Error searching LinkedIn jobs: {str(e)}")
        return {
            "status": "error",
            "user_id": user_id,
            "message": f"Error searching LinkedIn jobs: {str(e)}"
        }
    finally:
        db.close()


@celery_app.task(bind=True, name="linkedin.apply_to_job")
def apply_to_job(
    self, 
    user_id: str, 
    job_id: str,
    resume_id: Optional[str] = None,
    cover_letter_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Apply to a job on LinkedIn.
    
    Args:
        user_id: The ID of the user applying to the job
        job_id: The ID of the job to apply to
        resume_id: The ID of the resume to use
        cover_letter_id: The ID of the cover letter to use
        
    Returns:
        Dict containing the result of the application
    """
    logger.info(f"Applying to LinkedIn job {job_id} for user {user_id}")
    
    # Note: LinkedIn's API doesn't directly support job applications
    # This would typically redirect users to the LinkedIn application page
    # or use LinkedIn's "Apply with LinkedIn" feature
    
    db = SessionLocal()
    try:
        # Get user and job
        user = get_user(db, user_id=user_id)
        if not user:
            return {
                "status": "error",
                "user_id": user_id,
                "job_id": job_id,
                "message": "User not found"
            }
        
        job = get_job_by_linkedin_id(db, linkedin_job_id=job_id)
        if not job:
            return {
                "status": "error",
                "user_id": user_id,
                "job_id": job_id,
                "message": "Job not found"
            }
        
        # For now, return the apply URL
        return {
            "status": "success",
            "user_id": user_id,
            "job_id": job_id,
            "message": "Job application URL generated",
            "apply_url": job.apply_url
        }
    except Exception as e:
        logger.error(f"Error applying to LinkedIn job: {str(e)}")
        return {
            "status": "error",
            "user_id": user_id,
            "job_id": job_id,
            "message": f"Error applying to LinkedIn job: {str(e)}"
        }
    finally:
        db.close() 