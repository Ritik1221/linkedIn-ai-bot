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
from src.app.services.linkedin import get_linkedin_service
from src.app.services.vector_store import get_vector_store_service
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
        
        # Use the LinkedIn service to sync profile
        linkedin_service = get_linkedin_service(db)
        result = linkedin_service.sync_profile(user)
        
        # If profile sync was successful, index profile in vector store
        if result.get("status") == "success" and result.get("profile_id"):
            profile_id = result.get("profile_id")
            profile = db.query(Profile).filter(Profile.id == profile_id).first()
            if profile:
                vector_store = get_vector_store_service(db)
                vector_store.index_profile(profile)
        
        return result
    except Exception as e:
        logger.error(f"Error syncing LinkedIn profile: {str(e)}")
        return {
            "status": "error",
            "user_id": user_id,
            "message": f"Error syncing LinkedIn profile: {str(e)}"
        }
    finally:
        db.close()

@celery_app.task(bind=True, name="linkedin.sync_connections")
def sync_connections(self, user_id: str) -> Dict[str, Any]:
    """
    Synchronize a user's LinkedIn connections.
    
    Args:
        user_id: The ID of the user whose connections to sync
        
    Returns:
        Dict containing the result of the sync operation
    """
    logger.info(f"Syncing LinkedIn connections for user {user_id}")
    
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
        
        # Use the LinkedIn service to get connections
        linkedin_service = get_linkedin_service(db)
        
        # Get first page of connections
        page = 1
        limit = 100
        total_connections = []
        
        while True:
            result = linkedin_service.get_connections(user, page=page, limit=limit)
            
            if result.get("status") != "success":
                return result
            
            connections = result.get("connections", [])
            total_connections.extend(connections)
            
            # If we got fewer connections than the limit, we've reached the end
            if len(connections) < limit:
                break
            
            # Get next page
            page += 1
        
        return {
            "status": "success",
            "user_id": user_id,
            "count": len(total_connections),
            "message": f"Successfully synced {len(total_connections)} connections"
        }
    except Exception as e:
        logger.error(f"Error syncing LinkedIn connections: {str(e)}")
        return {
            "status": "error",
            "user_id": user_id,
            "message": f"Error syncing LinkedIn connections: {str(e)}"
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
    limit: int = 100
) -> Dict[str, Any]:
    """
    Search for jobs on LinkedIn.
    
    Args:
        user_id: The ID of the user performing the search
        keywords: Job keywords to search for
        location: Location to search in
        job_type: Type of job (full-time, part-time, etc.)
        experience_level: Experience level required
        limit: Maximum number of results to return
        
    Returns:
        Dict containing the job search results
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
        
        # Use the LinkedIn service to search jobs
        linkedin_service = get_linkedin_service(db)
        result = linkedin_service.search_jobs(
            user=user,
            keywords=keywords,
            location=location,
            job_type=job_type,
            experience_level=experience_level,
            limit=limit
        )
        
        # If job search was successful, index jobs in vector store
        if result.get("status") == "success" and result.get("jobs"):
            vector_store = get_vector_store_service(db)
            jobs = result.get("jobs", [])
            
            # Index each job
            for job_data in jobs:
                job_id = job_data.get("id")
                job = db.query(Job).filter(Job.id == job_id).first()
                if job:
                    vector_store.index_job(job)
        
        return result
    except Exception as e:
        logger.error(f"Error searching LinkedIn jobs: {str(e)}")
        return {
            "status": "error",
            "user_id": user_id,
            "message": f"Error searching LinkedIn jobs: {str(e)}"
        }
    finally:
        db.close()

@celery_app.task(bind=True, name="linkedin.find_matching_jobs")
def find_matching_jobs(self, user_id: str, limit: int = 20) -> Dict[str, Any]:
    """
    Find jobs that match a user's profile using vector search and LLM matching.
    
    Args:
        user_id: The ID of the user
        limit: Maximum number of results to return
        
    Returns:
        Dict containing matching jobs with scores
    """
    logger.info(f"Finding matching jobs for user {user_id}")
    
    db = SessionLocal()
    try:
        # Check if user exists
        user = get_user(db, user_id=user_id)
        if not user:
            return {
                "status": "error",
                "user_id": user_id,
                "message": "User not found"
            }
        
        # Use automation service to find matching jobs
        from src.app.services.automation import get_automation_service
        automation_service = get_automation_service(db)
        
        result = automation_service.find_matching_jobs(user_id=user_id, limit=limit)
        return result
    except Exception as e:
        logger.error(f"Error finding matching jobs: {str(e)}")
        return {
            "status": "error",
            "user_id": user_id,
            "message": f"Error finding matching jobs: {str(e)}"
        }
    finally:
        db.close()

@celery_app.task(bind=True, name="linkedin.bulk_index_jobs")
def bulk_index_jobs(self) -> Dict[str, Any]:
    """
    Index all jobs in the vector store.
    
    Returns:
        Dict containing the result of the indexing operation
    """
    logger.info("Indexing all jobs in vector store")
    
    db = SessionLocal()
    try:
        vector_store = get_vector_store_service(db)
        success_count, total_count = vector_store.reindex_all_jobs()
        
        return {
            "status": "success",
            "success_count": success_count,
            "total_count": total_count,
            "message": f"Successfully indexed {success_count}/{total_count} jobs"
        }
    except Exception as e:
        logger.error(f"Error indexing jobs: {str(e)}")
        return {
            "status": "error",
            "message": f"Error indexing jobs: {str(e)}"
        }
    finally:
        db.close()

@celery_app.task(bind=True, name="linkedin.bulk_index_profiles")
def bulk_index_profiles(self) -> Dict[str, Any]:
    """
    Index all profiles in the vector store.
    
    Returns:
        Dict containing the result of the indexing operation
    """
    logger.info("Indexing all profiles in vector store")
    
    db = SessionLocal()
    try:
        vector_store = get_vector_store_service(db)
        success_count, total_count = vector_store.reindex_all_profiles()
        
        return {
            "status": "success",
            "success_count": success_count,
            "total_count": total_count,
            "message": f"Successfully indexed {success_count}/{total_count} profiles"
        }
    except Exception as e:
        logger.error(f"Error indexing profiles: {str(e)}")
        return {
            "status": "error",
            "message": f"Error indexing profiles: {str(e)}"
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
    logger.info(f"Applying to job {job_id} for user {user_id}")
    
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
        
        # Use the LinkedIn service to apply to job
        linkedin_service = get_linkedin_service(db)
        result = linkedin_service.apply_to_job(
            user=user,
            job_id=job_id,
            resume_id=resume_id,
            cover_letter_id=cover_letter_id
        )
        
        return result
    except Exception as e:
        logger.error(f"Error applying to job: {str(e)}")
        return {
            "status": "error",
            "user_id": user_id,
            "job_id": job_id,
            "message": f"Error applying to job: {str(e)}"
        }
    finally:
        db.close() 