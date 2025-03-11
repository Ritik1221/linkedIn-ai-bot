"""
LLM-related Celery tasks for the LinkedIn AI Agent.
"""

import logging
from typing import Dict, Any, List, Optional

from src.app.core.llm_client import get_llm_client
from src.app.db.session import SessionLocal
from src.app.models.user import User
from src.app.models.profile import Profile
from src.app.models.job import Job
from src.app.services.user import get_user
from src.app.services.profile import get_profile_by_user, update_profile
from src.app.services.job import get_job
from src.worker.main import celery_app

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, name="llm.analyze_profile")
def analyze_profile(self, user_id: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze a LinkedIn profile using LLM.
    
    Args:
        user_id: The ID of the user whose profile to analyze
        profile_data: The LinkedIn profile data to analyze
        
    Returns:
        Dict containing the analysis results
    """
    logger.info(f"Analyzing LinkedIn profile for user {user_id}")
    
    db = SessionLocal()
    try:
        # Get LLM client
        llm_client = get_llm_client()
        
        # Analyze profile
        analysis = llm_client.analyze_profile(profile_data)
        
        # Update profile with analysis
        profile = get_profile_by_user(db, user_id=user_id)
        if profile:
            update_profile(db, profile=profile, profile_in={
                "analysis": analysis,
                "analyzed_at": "now()"
            })
        
        return {
            "status": "success",
            "user_id": user_id,
            "message": "Profile analyzed successfully",
            "analysis": analysis
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
def match_job(
    self, 
    user_id: str, 
    profile_data: Dict[str, Any],
    job_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Match a job to a user's profile using LLM.
    
    Args:
        user_id: The ID of the user
        profile_data: The user's LinkedIn profile data
        job_data: The job data to match against
        
    Returns:
        Dict containing the match results
    """
    logger.info(f"Matching job to profile for user {user_id}")
    
    db = SessionLocal()
    try:
        # Get LLM client
        llm_client = get_llm_client()
        
        # Match job to profile
        match_results = llm_client.match_job(profile_data, job_data)
        
        # Store match results (could be stored in a separate table)
        
        return {
            "status": "success",
            "user_id": user_id,
            "job_id": job_data.get("id", "unknown"),
            "message": "Job matched successfully",
            "match_results": match_results
        }
    except Exception as e:
        logger.error(f"Error matching job: {str(e)}")
        return {
            "status": "error",
            "user_id": user_id,
            "job_id": job_data.get("id", "unknown"),
            "message": f"Error matching job: {str(e)}"
        }
    finally:
        db.close()

@celery_app.task(bind=True, name="llm.generate_cover_letter")
def generate_cover_letter(
    self, 
    user_id: str, 
    profile_data: Dict[str, Any],
    job_data: Dict[str, Any],
    customization_notes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate a cover letter for a job application using LLM.
    
    Args:
        user_id: The ID of the user
        profile_data: The user's LinkedIn profile data
        job_data: The job data to apply for
        customization_notes: Additional notes for customization
        
    Returns:
        Dict containing the generated cover letter
    """
    logger.info(f"Generating cover letter for user {user_id}")
    
    db = SessionLocal()
    try:
        # Get LLM client
        llm_client = get_llm_client()
        
        # Generate cover letter
        cover_letter = llm_client.generate_cover_letter(
            profile_data, 
            job_data, 
            customization_notes
        )
        
        return {
            "status": "success",
            "user_id": user_id,
            "job_id": job_data.get("id", "unknown"),
            "message": "Cover letter generated successfully",
            "cover_letter": cover_letter
        }
    except Exception as e:
        logger.error(f"Error generating cover letter: {str(e)}")
        return {
            "status": "error",
            "user_id": user_id,
            "job_id": job_data.get("id", "unknown"),
            "message": f"Error generating cover letter: {str(e)}"
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
        # Get LLM client
        llm_client = get_llm_client()
        
        # Get user and recipient profiles
        user = get_user(db, user_id=user_id)
        recipient = get_user(db, user_id=recipient_id)
        
        if not user or not recipient:
            return {
                "status": "error",
                "user_id": user_id,
                "recipient_id": recipient_id,
                "message": "User or recipient not found"
            }
        
        # Create prompt based on message type
        if message_type == "connection_request":
            prompt = f"""
            Generate a personalized LinkedIn connection request message from {user.full_name} to {recipient.full_name}.
            
            Context information:
            {context}
            
            The message should be professional, concise (max 300 characters), and include:
            1. A personalized greeting
            2. A brief explanation of why they want to connect
            3. A reference to shared interests or experiences if available
            4. A polite closing
            
            Format your response as plain text, ready to be sent as a connection request.
            """
        elif message_type == "follow_up":
            prompt = f"""
            Generate a personalized follow-up message from {user.full_name} to {recipient.full_name}.
            
            Context information:
            {context}
            
            The message should be professional, concise, and include:
            1. A reference to their previous interaction
            2. The main purpose of the follow-up
            3. A clear call to action
            4. A polite closing
            
            Format your response as plain text, ready to be sent as a message.
            """
        else:
            prompt = f"""
            Generate a personalized message from {user.full_name} to {recipient.full_name}.
            
            Context information:
            {context}
            
            The message should be professional, concise, and appropriate for the context.
            
            Format your response as plain text, ready to be sent as a message.
            """
        
        system_prompt = "You are an expert at writing professional, personalized networking messages. Create messages that are authentic, concise, and effective."
        
        # Generate message
        message = llm_client.generate_text(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=500,
            temperature=0.7,
        )
        
        return {
            "status": "success",
            "user_id": user_id,
            "recipient_id": recipient_id,
            "message_type": message_type,
            "generated_message": message
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