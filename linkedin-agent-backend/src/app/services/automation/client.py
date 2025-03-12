"""
Automation client for the LinkedIn AI Agent.
This module provides functions for automating job applications and resume customization.
"""

import logging
import os
import time
from typing import Any, Dict, List, Optional, Tuple, Union

from sqlalchemy.orm import Session

from src.app.core.config import settings
from src.app.db.session import SessionLocal
from src.app.models.profile import Profile
from src.app.models.job import Job
from src.app.models.user import User
from src.app.models.application import Application, Resume, CoverLetter
from src.app.services.llm import get_llm_service
from src.app.services.vector_store import get_vector_store_service

logger = logging.getLogger(__name__)


class AutomationService:
    """Automation service for resume customization and job applications."""

    def __init__(self, db: Session = None):
        """
        Initialize the automation service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.llm_service = get_llm_service(db)
        self.vector_store = get_vector_store_service(db)

    def generate_resume(
        self,
        user_id: str,
        job_id: str,
        customization_notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a tailored resume for a job application.
        
        Args:
            user_id: User ID
            job_id: Job ID
            customization_notes: Additional notes for customization
            
        Returns:
            Dictionary with generated resume information
        """
        logger.info(f"Generating resume for user {user_id} and job {job_id}")
        
        try:
            # Get user profile
            profile = self.db.query(Profile).filter(Profile.user_id == user_id).first()
            if not profile:
                return {
                    "status": "error",
                    "message": "User profile not found"
                }
            
            # Get job
            job = self.db.query(Job).filter(Job.id == job_id).first()
            if not job:
                return {
                    "status": "error",
                    "message": "Job not found"
                }
            
            # Create profile data
            profile_data = self._create_profile_data(profile)
            
            # Create job data
            job_data = {
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "description": job.description
            }
            
            # Get resume recommendations
            recommendations = self.llm_service.tailor_resume(
                profile_data=profile_data,
                job_data=job_data,
                customization_notes=customization_notes
            )
            
            # Create resume record
            resume = Resume(
                user_id=user_id,
                job_id=job_id,
                content=recommendations,
                created_at="NOW()"
            )
            self.db.add(resume)
            self.db.commit()
            
            return {
                "status": "success",
                "resume_id": resume.id,
                "recommendations": recommendations,
                "message": "Resume recommendations generated successfully"
            }
        except Exception as e:
            logger.error(f"Error generating resume: {str(e)}")
            return {
                "status": "error",
                "message": f"Error generating resume: {str(e)}"
            }

    def generate_cover_letter(
        self,
        user_id: str,
        job_id: str,
        customization_notes: Optional[str] = None,
        tone: str = "professional"
    ) -> Dict[str, Any]:
        """
        Generate a cover letter for a job application.
        
        Args:
            user_id: User ID
            job_id: Job ID
            customization_notes: Additional notes for customization
            tone: Tone of the cover letter (professional, conversational, enthusiastic)
            
        Returns:
            Dictionary with generated cover letter
        """
        logger.info(f"Generating cover letter for user {user_id} and job {job_id}")
        
        try:
            # Get user profile
            profile = self.db.query(Profile).filter(Profile.user_id == user_id).first()
            if not profile:
                return {
                    "status": "error",
                    "message": "User profile not found"
                }
            
            # Get job
            job = self.db.query(Job).filter(Job.id == job_id).first()
            if not job:
                return {
                    "status": "error",
                    "message": "Job not found"
                }
            
            # Create profile data
            profile_data = self._create_profile_data(profile)
            
            # Create job data
            job_data = {
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "description": job.description
            }
            
            # Generate cover letter
            cover_letter_content = self.llm_service.generate_cover_letter(
                profile_data=profile_data,
                job_data=job_data,
                customization_notes=customization_notes,
                tone=tone
            )
            
            # Create cover letter record
            cover_letter = CoverLetter(
                user_id=user_id,
                job_id=job_id,
                content=cover_letter_content,
                created_at="NOW()"
            )
            self.db.add(cover_letter)
            self.db.commit()
            
            return {
                "status": "success",
                "cover_letter_id": cover_letter.id,
                "cover_letter": cover_letter_content,
                "message": "Cover letter generated successfully"
            }
        except Exception as e:
            logger.error(f"Error generating cover letter: {str(e)}")
            return {
                "status": "error",
                "message": f"Error generating cover letter: {str(e)}"
            }

    def find_matching_jobs(self, user_id: str, limit: int = 10) -> Dict[str, Any]:
        """
        Find jobs that match a user's profile.
        
        Args:
            user_id: User ID
            limit: Maximum number of results
            
        Returns:
            Dictionary with matching jobs
        """
        logger.info(f"Finding matching jobs for user {user_id}")
        
        try:
            # Get user profile
            profile = self.db.query(Profile).filter(Profile.user_id == user_id).first()
            if not profile:
                return {
                    "status": "error",
                    "message": "User profile not found"
                }
            
            # Find similar jobs
            similar_jobs = self.vector_store.find_similar_jobs(
                profile_id=profile.id,
                limit=limit
            )
            
            # Get detailed job info
            matching_jobs = []
            for job_match in similar_jobs:
                job_id = job_match["id"]
                job = self.db.query(Job).filter(Job.id == job_id).first()
                if job:
                    # Get job match score from LLM
                    profile_data = self._create_profile_data(profile)
                    job_data = {
                        "id": job.id,
                        "title": job.title,
                        "company": job.company,
                        "location": job.location,
                        "description": job.description
                    }
                    
                    match_result = self.llm_service.match_job(
                        profile_data=profile_data,
                        job_data=job_data
                    )
                    
                    # Combine vector and LLM scores
                    vector_score = job_match["score"]
                    llm_score = match_result.get("match_score", 50) / 100.0  # Normalize to 0-1
                    combined_score = (vector_score + llm_score) / 2.0
                    
                    matching_jobs.append({
                        "id": job.id,
                        "title": job.title,
                        "company": job.company,
                        "location": job.location,
                        "score": combined_score,
                        "vector_score": vector_score,
                        "llm_score": llm_score,
                        "matching_points": match_result.get("matching_points", []),
                        "missing_points": match_result.get("missing_points", []),
                        "recommendations": match_result.get("recommendations", []),
                        "summary": match_result.get("summary", "")
                    })
            
            # Sort by score
            matching_jobs.sort(key=lambda x: x["score"], reverse=True)
            
            return {
                "status": "success",
                "count": len(matching_jobs),
                "jobs": matching_jobs,
                "message": f"Found {len(matching_jobs)} matching jobs"
            }
        except Exception as e:
            logger.error(f"Error finding matching jobs: {str(e)}")
            return {
                "status": "error",
                "message": f"Error finding matching jobs: {str(e)}"
            }

    def create_application(
        self,
        user_id: str,
        job_id: str,
        resume_id: Optional[str] = None,
        cover_letter_id: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a job application.
        
        Args:
            user_id: User ID
            job_id: Job ID
            resume_id: Resume ID
            cover_letter_id: Cover letter ID
            notes: Application notes
            
        Returns:
            Dictionary with application information
        """
        logger.info(f"Creating application for user {user_id} and job {job_id}")
        
        try:
            # Check if user exists
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return {
                    "status": "error",
                    "message": "User not found"
                }
            
            # Check if job exists
            job = self.db.query(Job).filter(Job.id == job_id).first()
            if not job:
                return {
                    "status": "error",
                    "message": "Job not found"
                }
            
            # Check if resume exists if provided
            if resume_id:
                resume = self.db.query(Resume).filter(Resume.id == resume_id).first()
                if not resume:
                    return {
                        "status": "error",
                        "message": "Resume not found"
                    }
            
            # Check if cover letter exists if provided
            if cover_letter_id:
                cover_letter = self.db.query(CoverLetter).filter(CoverLetter.id == cover_letter_id).first()
                if not cover_letter:
                    return {
                        "status": "error",
                        "message": "Cover letter not found"
                    }
            
            # Create application
            application = Application(
                user_id=user_id,
                job_id=job_id,
                resume_id=resume_id,
                cover_letter_id=cover_letter_id,
                status="prepared",
                notes=notes,
                created_at="NOW()"
            )
            self.db.add(application)
            self.db.commit()
            
            return {
                "status": "success",
                "application_id": application.id,
                "message": "Application created successfully"
            }
        except Exception as e:
            logger.error(f"Error creating application: {str(e)}")
            return {
                "status": "error",
                "message": f"Error creating application: {str(e)}"
            }

    def submit_application(
        self,
        application_id: str
    ) -> Dict[str, Any]:
        """
        Submit a job application.
        
        Args:
            application_id: Application ID
            
        Returns:
            Dictionary with submission result
        """
        logger.info(f"Submitting application {application_id}")
        
        try:
            # Get application
            application = self.db.query(Application).filter(Application.id == application_id).first()
            if not application:
                return {
                    "status": "error",
                    "message": "Application not found"
                }
            
            # Check application status
            if application.status not in ["prepared", "failed"]:
                return {
                    "status": "error",
                    "message": f"Application is in {application.status} status and cannot be submitted"
                }
            
            # Get job
            job = self.db.query(Job).filter(Job.id == application.job_id).first()
            if not job:
                return {
                    "status": "error",
                    "message": "Job not found"
                }
            
            # TODO: Implement actual submission logic
            # This would involve integration with LinkedIn or other job sites
            
            # Mock submission - in a real system this would use a LinkedIn API client
            success = True
            external_id = f"app_{int(time.time())}"
            
            if success:
                # Update application status
                application.status = "submitted"
                application.submitted_at = "NOW()"
                application.external_application_id = external_id
                self.db.add(application)
                self.db.commit()
                
                return {
                    "status": "success",
                    "application_id": application.id,
                    "external_id": external_id,
                    "message": "Application submitted successfully"
                }
            else:
                # Update application status
                application.status = "failed"
                self.db.add(application)
                self.db.commit()
                
                return {
                    "status": "error",
                    "message": "Failed to submit application"
                }
        except Exception as e:
            logger.error(f"Error submitting application: {str(e)}")
            return {
                "status": "error",
                "message": f"Error submitting application: {str(e)}"
            }

    def get_application_status(
        self,
        application_id: str
    ) -> Dict[str, Any]:
        """
        Get the status of a job application.
        
        Args:
            application_id: Application ID
            
        Returns:
            Dictionary with application status
        """
        logger.info(f"Getting status for application {application_id}")
        
        try:
            # Get application
            application = self.db.query(Application).filter(Application.id == application_id).first()
            if not application:
                return {
                    "status": "error",
                    "message": "Application not found"
                }
            
            # Get job
            job = self.db.query(Job).filter(Job.id == application.job_id).first()
            
            # Get status info
            result = {
                "status": "success",
                "application_id": application.id,
                "application_status": application.status,
                "job_id": application.job_id,
                "job_title": job.title if job else "Unknown",
                "job_company": job.company if job else "Unknown",
                "created_at": application.created_at,
                "submitted_at": application.submitted_at,
                "external_application_id": application.external_application_id,
                "resume_id": application.resume_id,
                "cover_letter_id": application.cover_letter_id,
                "notes": application.notes
            }
            
            return result
        except Exception as e:
            logger.error(f"Error getting application status: {str(e)}")
            return {
                "status": "error",
                "message": f"Error getting application status: {str(e)}"
            }

    def get_user_applications(
        self,
        user_id: str,
        status: Optional[str] = None,
        page: int = 1,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Get applications for a user.
        
        Args:
            user_id: User ID
            status: Filter by status
            page: Page number
            limit: Results per page
            
        Returns:
            Dictionary with applications
        """
        logger.info(f"Getting applications for user {user_id}")
        
        try:
            # Build query
            query = self.db.query(Application).filter(Application.user_id == user_id)
            
            # Filter by status if provided
            if status:
                query = query.filter(Application.status == status)
            
            # Get total count
            total_count = query.count()
            
            # Paginate
            offset = (page - 1) * limit
            applications = query.order_by(Application.created_at.desc()).offset(offset).limit(limit).all()
            
            # Format results
            result_applications = []
            for app in applications:
                # Get job
                job = self.db.query(Job).filter(Job.id == app.job_id).first()
                
                result_applications.append({
                    "id": app.id,
                    "job_id": app.job_id,
                    "job_title": job.title if job else "Unknown",
                    "job_company": job.company if job else "Unknown",
                    "status": app.status,
                    "created_at": app.created_at,
                    "submitted_at": app.submitted_at,
                    "has_resume": app.resume_id is not None,
                    "has_cover_letter": app.cover_letter_id is not None
                })
            
            return {
                "status": "success",
                "total": total_count,
                "page": page,
                "limit": limit,
                "applications": result_applications,
                "message": f"Retrieved {len(result_applications)} applications"
            }
        except Exception as e:
            logger.error(f"Error getting user applications: {str(e)}")
            return {
                "status": "error",
                "message": f"Error getting user applications: {str(e)}"
            }

    def _create_profile_data(self, profile: Profile) -> Dict[str, Any]:
        """
        Create a dictionary representation of a profile.
        
        Args:
            profile: Profile object
            
        Returns:
            Dictionary representation
        """
        # Get experiences
        experiences = []
        if hasattr(profile, "experiences") and profile.experiences:
            for exp in profile.experiences:
                experiences.append({
                    "title": exp.title,
                    "company": exp.company,
                    "location": exp.location,
                    "description": exp.description,
                    "start_date": exp.start_date,
                    "end_date": exp.end_date,
                    "is_current": exp.is_current
                })
        
        # Get education
        education = []
        if hasattr(profile, "education") and profile.education:
            for edu in profile.education:
                education.append({
                    "school": edu.school,
                    "degree": edu.degree,
                    "field_of_study": edu.field_of_study,
                    "start_date": edu.start_date,
                    "end_date": edu.end_date,
                    "description": edu.description
                })
        
        # Get skills
        skills = []
        if hasattr(profile, "skills") and profile.skills:
            for skill in profile.skills:
                skills.append({
                    "name": skill.name,
                    "endorsements": skill.endorsements
                })
        
        # Get certifications
        certifications = []
        if hasattr(profile, "certifications") and profile.certifications:
            for cert in profile.certifications:
                certifications.append({
                    "name": cert.name,
                    "issuing_organization": cert.issuing_organization,
                    "issue_date": cert.issue_date,
                    "expiration_date": cert.expiration_date,
                    "credential_id": cert.credential_id
                })
        
        # Create profile data
        return {
            "id": profile.id,
            "user_id": profile.user_id,
            "full_name": profile.full_name,
            "headline": profile.headline,
            "summary": profile.summary,
            "profile_picture_url": profile.profile_picture_url,
            "linkedin_profile_url": profile.linkedin_profile_url,
            "linkedin_id": profile.linkedin_id,
            "experiences": experiences,
            "education": education,
            "skills": skills,
            "certifications": certifications
        }


def get_automation_service(db: Session = None) -> AutomationService:
    """
    Get an automation service instance.
    
    Args:
        db: Database session
        
    Returns:
        Automation service instance
    """
    if db is None:
        db = SessionLocal()
    return AutomationService(db=db) 