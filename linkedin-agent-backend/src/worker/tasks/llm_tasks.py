"""
LLM-related Celery tasks for the LinkedIn AI Agent.
"""

import logging
from typing import Dict, Any, List, Optional

from src.app.db.session import SessionLocal
from src.app.models.user import User
from src.app.models.profile import Profile
from src.app.models.job import Job
from src.app.services.user import get_user
from src.app.services.profile import get_profile_by_user, update_profile
from src.app.services.job import get_job
from src.app.services.llm import get_llm_service
from src.app.services.automation import get_automation_service
from src.worker.main import celery_app

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, name="llm.analyze_profile")
def analyze_profile(self, user_id: str) -> Dict[str, Any]:
    """
    Analyze a LinkedIn profile using LLM.
    
    Args:
        user_id: The ID of the user whose profile to analyze
        
    Returns:
        Dict containing the analysis results
    """
    logger.info(f"Analyzing LinkedIn profile for user {user_id}")
    
    db = SessionLocal()
    try:
        # Get profile
        profile = get_profile_by_user(db, user_id=user_id)
        if not profile:
            return {
                "status": "error",
                "user_id": user_id,
                "message": "Profile not found"
            }
        
        # Create profile data
        profile_data = _create_profile_data(profile)
        
        # Use LLM service for analysis
        llm_service = get_llm_service(db)
        analysis = llm_service.analyze_profile(profile_data)
        
        # Update profile with analysis
        update_profile(db, profile=profile, profile_in={
            "analysis": analysis,
            "analyzed_at": "NOW()"
        })
        
        return {
            "status": "success",
            "user_id": user_id,
            "profile_id": str(profile.id),
            "analysis": analysis,
            "message": "Profile analyzed successfully"
        }
    except Exception as e:
        logger.error(f"Error analyzing profile: {str(e)}")
        return {
            "status": "error",
            "user_id": user_id,
            "message": f"Error analyzing profile: {str(e)}"
        }
    finally:
        db.close()

@celery_app.task(bind=True, name="llm.match_job")
def match_job(self, user_id: str, job_id: str) -> Dict[str, Any]:
    """
    Match a profile to a job using LLM.
    
    Args:
        user_id: The ID of the user whose profile to match
        job_id: The ID of the job to match against
        
    Returns:
        Dict containing the match results
    """
    logger.info(f"Matching user {user_id} to job {job_id}")
    
    db = SessionLocal()
    try:
        # Get profile
        profile = get_profile_by_user(db, user_id=user_id)
        if not profile:
            return {
                "status": "error",
                "user_id": user_id,
                "job_id": job_id,
                "message": "Profile not found"
            }
        
        # Get job
        job = get_job(db, job_id=job_id)
        if not job:
            return {
                "status": "error",
                "user_id": user_id,
                "job_id": job_id,
                "message": "Job not found"
            }
        
        # Create profile data
        profile_data = _create_profile_data(profile)
        
        # Create job data
        job_data = {
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "description": job.description
        }
        
        # Use LLM service for job matching
        llm_service = get_llm_service(db)
        match_result = llm_service.match_job(profile_data, job_data)
        
        return {
            "status": "success",
            "user_id": user_id,
            "job_id": job_id,
            "match_result": match_result,
            "message": "Job match completed successfully"
        }
    except Exception as e:
        logger.error(f"Error matching job: {str(e)}")
        return {
            "status": "error",
            "user_id": user_id,
            "job_id": job_id,
            "message": f"Error matching job: {str(e)}"
        }
    finally:
        db.close()

@celery_app.task(bind=True, name="llm.generate_cover_letter")
def generate_cover_letter(
    self, 
    user_id: str, 
    job_id: str,
    customization_notes: Optional[str] = None,
    tone: str = "professional"
) -> Dict[str, Any]:
    """
    Generate a cover letter for a job application using LLM.
    
    Args:
        user_id: The ID of the user applying for the job
        job_id: The ID of the job to apply for
        customization_notes: Additional notes for customization
        tone: Tone of the cover letter (professional, conversational, enthusiastic)
        
    Returns:
        Dict containing the generated cover letter
    """
    logger.info(f"Generating cover letter for user {user_id} and job {job_id}")
    
    db = SessionLocal()
    try:
        # Use automation service to generate cover letter
        automation_service = get_automation_service(db)
        result = automation_service.generate_cover_letter(
            user_id=user_id,
            job_id=job_id,
            customization_notes=customization_notes,
            tone=tone
        )
        
        return result
    except Exception as e:
        logger.error(f"Error generating cover letter: {str(e)}")
        return {
            "status": "error",
            "user_id": user_id,
            "job_id": job_id,
            "message": f"Error generating cover letter: {str(e)}"
        }
    finally:
        db.close()

@celery_app.task(bind=True, name="llm.generate_resume")
def generate_resume(
    self, 
    user_id: str, 
    job_id: str,
    customization_notes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate a tailored resume for a job application using LLM.
    
    Args:
        user_id: The ID of the user applying for the job
        job_id: The ID of the job to apply for
        customization_notes: Additional notes for customization
        
    Returns:
        Dict containing the generated resume recommendations
    """
    logger.info(f"Generating resume for user {user_id} and job {job_id}")
    
    db = SessionLocal()
    try:
        # Use automation service to generate resume
        automation_service = get_automation_service(db)
        result = automation_service.generate_resume(
            user_id=user_id,
            job_id=job_id,
            customization_notes=customization_notes
        )
        
        return result
    except Exception as e:
        logger.error(f"Error generating resume: {str(e)}")
        return {
            "status": "error",
            "user_id": user_id,
            "job_id": job_id,
            "message": f"Error generating resume: {str(e)}"
        }
    finally:
        db.close()

@celery_app.task(bind=True, name="llm.generate_message")
def generate_message(
    self, 
    user_id: str,
    recipient_id: str,
    context: Dict[str, Any],
    message_type: str = "connection_request"
) -> Dict[str, Any]:
    """
    Generate a personalized message using LLM.
    
    Args:
        user_id: The ID of the user sending the message
        recipient_id: The ID of the message recipient
        context: Context information for message generation
        message_type: Type of message to generate
        
    Returns:
        Dict containing the generated message
    """
    logger.info(f"Generating {message_type} message for user {user_id} to recipient {recipient_id}")
    
    db = SessionLocal()
    try:
        # Get sender profile
        sender_profile = get_profile_by_user(db, user_id=user_id)
        if not sender_profile:
            return {
                "status": "error",
                "user_id": user_id,
                "recipient_id": recipient_id,
                "message": "Sender profile not found"
            }
        
        # Get recipient profile
        recipient_profile = get_profile_by_user(db, user_id=recipient_id)
        if not recipient_profile:
            return {
                "status": "error",
                "user_id": user_id,
                "recipient_id": recipient_id,
                "message": "Recipient profile not found"
            }
        
        # Create sender data
        sender_data = _create_profile_data(sender_profile)
        
        # Create recipient data
        recipient_data = _create_profile_data(recipient_profile)
        
        # Use LLM service to generate message
        llm_service = get_llm_service(db)
        message = llm_service.generate_message(
            sender_data=sender_data,
            recipient_data=recipient_data,
            context=context,
            message_type=message_type
        )
        
        return {
            "status": "success",
            "user_id": user_id,
            "recipient_id": recipient_id,
            "message_type": message_type,
            "generated_message": message,
            "message": "Message generated successfully"
        }
    except Exception as e:
        logger.error(f"Error generating message: {str(e)}")
        return {
            "status": "error",
            "user_id": user_id,
            "recipient_id": recipient_id,
            "message": f"Error generating message: {str(e)}"
        }
    finally:
        db.close()

@celery_app.task(bind=True, name="llm.prepare_interview")
def prepare_interview(
    self, 
    user_id: str, 
    job_id: str,
    interview_type: str = "behavioral"
) -> Dict[str, Any]:
    """
    Prepare interview materials using LLM.
    
    Args:
        user_id: The ID of the user preparing for the interview
        job_id: The ID of the job being interviewed for
        interview_type: Type of interview (behavioral, technical, case)
        
    Returns:
        Dict containing the interview preparation materials
    """
    logger.info(f"Preparing {interview_type} interview for user {user_id} and job {job_id}")
    
    db = SessionLocal()
    try:
        # Get profile
        profile = get_profile_by_user(db, user_id=user_id)
        if not profile:
            return {
                "status": "error",
                "user_id": user_id,
                "job_id": job_id,
                "message": "Profile not found"
            }
        
        # Get job
        job = get_job(db, job_id=job_id)
        if not job:
            return {
                "status": "error",
                "user_id": user_id,
                "job_id": job_id,
                "message": "Job not found"
            }
        
        # Create profile data
        profile_data = _create_profile_data(profile)
        
        # Create job data
        job_data = {
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "description": job.description
        }
        
        # Use LLM service to prepare interview
        llm_service = get_llm_service(db)
        interview_prep = llm_service.prepare_interview(
            profile_data=profile_data,
            job_data=job_data,
            interview_type=interview_type
        )
        
        return {
            "status": "success",
            "user_id": user_id,
            "job_id": job_id,
            "interview_type": interview_type,
            "interview_prep": interview_prep,
            "message": "Interview preparation completed successfully"
        }
    except Exception as e:
        logger.error(f"Error preparing interview: {str(e)}")
        return {
            "status": "error",
            "user_id": user_id,
            "job_id": job_id,
            "message": f"Error preparing interview: {str(e)}"
        }
    finally:
        db.close()

def _create_profile_data(profile: Profile) -> Dict[str, Any]:
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