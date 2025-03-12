"""
LLM client service implementation.
This module provides comprehensive implementations for LLM operations.
"""

import json
import logging
import time
from typing import Any, Dict, List, Optional, Tuple, Union

from sqlalchemy.orm import Session

from src.app.core.llm_client import LLMClient, get_llm_client
from src.app.models.profile import Profile
from src.app.models.job import Job
from src.app.models.user import User
from src.app.db.session import SessionLocal

logger = logging.getLogger(__name__)


class LLMService:
    """LLM service for comprehensive AI operations."""

    def __init__(self, db: Session = None):
        """
        Initialize the LLM service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.client = get_llm_client()
        
        # Define system prompts
        self.system_prompts = {
            "profile_analysis": "You are an expert LinkedIn profile analyzer with expertise in career development and personal branding. Provide detailed, professional analysis of LinkedIn profiles.",
            "job_matching": "You are an expert job matcher and career advisor with deep knowledge of various industries. Provide detailed, professional analysis of how well a candidate matches a job posting.",
            "cover_letter": "You are an expert cover letter writer with extensive experience in professional writing and recruiting. Create personalized, compelling cover letters that highlight relevant skills and experiences.",
            "resume_tailoring": "You are an expert resume writer with deep knowledge of ATS systems and recruiting processes. Create tailored, effective resumes that highlight relevant skills and experiences.",
            "message_generation": "You are an expert networking professional with excellent communication skills. Generate personalized, effective messages for professional networking contexts.",
            "interview_prep": "You are an expert interview coach with extensive knowledge of various industries and roles. Provide detailed, personalized interview preparation guidance.",
        }

    def analyze_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a LinkedIn profile using LLM.
        
        Args:
            profile_data: LinkedIn profile data
            
        Returns:
            Dictionary with analysis results
        """
        logger.info("Analyzing LinkedIn profile")
        
        try:
            # Create prompt for profile analysis
            prompt = f"""
            Analyze the following LinkedIn profile and provide:
            1. Key strengths (skills, experiences, and qualities that stand out)
            2. Areas for improvement (gaps, weak points, or things to enhance)
            3. Specific recommendations to enhance the profile (concrete actions)
            4. Skills assessment (present skills, missing important skills, recommendations)
            5. Career trajectory analysis (past path, current position, future opportunities)
            
            Profile data:
            {json.dumps(profile_data, indent=2)}
            
            Format your response as JSON with the following structure:
            {{
                "strengths": ["strength1", "strength2", ...],
                "improvement_areas": ["area1", "area2", ...],
                "recommendations": ["recommendation1", "recommendation2", ...],
                "skills_assessment": {{
                    "present": ["skill1", "skill2", ...],
                    "missing": ["skill1", "skill2", ...],
                    "recommendations": ["recommendation1", "recommendation2", ...]
                }},
                "career_trajectory": {{
                    "past": "Analysis of past roles and progression",
                    "current": "Analysis of current position",
                    "future": "Potential future opportunities and paths"
                }}
            }}
            """
            
            # Get analysis from LLM
            response = self.client.generate_text(
                prompt=prompt,
                system_prompt=self.system_prompts["profile_analysis"],
                max_tokens=2000,
                temperature=0.3,
            )
            
            try:
                # Parse JSON response
                analysis = json.loads(response)
                return analysis
            except json.JSONDecodeError:
                # Handle parsing error
                logger.error("Failed to parse LLM response as JSON")
                return {
                    "strengths": ["Could not parse strengths"],
                    "improvement_areas": ["Could not parse improvement areas"],
                    "recommendations": ["Could not parse recommendations"],
                    "skills_assessment": {
                        "present": ["Could not parse present skills"],
                        "missing": ["Could not parse missing skills"],
                        "recommendations": ["Could not parse skill recommendations"]
                    },
                    "career_trajectory": {
                        "past": "Could not parse past trajectory",
                        "current": "Could not parse current position",
                        "future": "Could not parse future opportunities"
                    },
                    "raw_response": response
                }
        except Exception as e:
            logger.error(f"Error analyzing LinkedIn profile: {str(e)}")
            return {
                "status": "error",
                "message": f"Error analyzing LinkedIn profile: {str(e)}"
            }

    def match_job(
        self, 
        profile_data: Dict[str, Any],
        job_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Match a profile to a job using LLM.
        
        Args:
            profile_data: LinkedIn profile data
            job_data: Job data
            
        Returns:
            Dictionary with match results
        """
        logger.info("Matching profile to job")
        
        try:
            # Create prompt for job matching
            prompt = f"""
            Analyze how well the following candidate profile matches the job posting.
            
            Profile data:
            {json.dumps(profile_data, indent=2)}
            
            Job posting:
            {json.dumps(job_data, indent=2)}
            
            Provide:
            1. A match score (0-100)
            2. Key matching points (skills, experiences that align with the job)
            3. Missing requirements (skills, experiences the candidate lacks)
            4. Recommendations for the candidate to improve their fit
            5. A summary of the overall match
            
            Format your response as JSON with the following structure:
            {{
                "match_score": 75,
                "matching_points": ["point1", "point2", ...],
                "missing_points": ["point1", "point2", ...],
                "recommendations": ["recommendation1", "recommendation2", ...],
                "summary": "Overall assessment of the match"
            }}
            """
            
            # Get analysis from LLM
            response = self.client.generate_text(
                prompt=prompt,
                system_prompt=self.system_prompts["job_matching"],
                max_tokens=2000,
                temperature=0.3,
            )
            
            try:
                # Parse JSON response
                match_results = json.loads(response)
                return match_results
            except json.JSONDecodeError:
                # Handle parsing error
                logger.error("Failed to parse LLM response as JSON")
                return {
                    "match_score": 50,
                    "matching_points": ["Could not parse matching points"],
                    "missing_points": ["Could not parse missing points"],
                    "recommendations": ["Could not parse recommendations"],
                    "summary": "Could not generate a proper match analysis",
                    "raw_response": response
                }
        except Exception as e:
            logger.error(f"Error matching profile to job: {str(e)}")
            return {
                "status": "error",
                "message": f"Error matching profile to job: {str(e)}"
            }

    def generate_cover_letter(
        self,
        profile_data: Dict[str, Any],
        job_data: Dict[str, Any],
        customization_notes: Optional[str] = None,
        tone: str = "professional"
    ) -> Dict[str, Any]:
        """
        Generate a cover letter for a job application using LLM.
        
        Args:
            profile_data: LinkedIn profile data
            job_data: Job data
            customization_notes: Additional notes for customization
            tone: Tone of the cover letter (professional, conversational, enthusiastic)
            
        Returns:
            Dictionary with generated cover letter
        """
        logger.info("Generating cover letter")
        
        try:
            # Create prompt for cover letter generation
            prompt = f"""
            Generate a professional cover letter for a job application based on the following:
            
            Profile data:
            {json.dumps(profile_data, indent=2)}
            
            Job posting:
            {json.dumps(job_data, indent=2)}
            
            Tone: {tone}
            """
            
            if customization_notes:
                prompt += f"\n\nAdditional customization notes:\n{customization_notes}"
            
            prompt += """
            
            Format your response as JSON with the following structure:
            {
                "subject_line": "Subject line for the application email",
                "salutation": "Dear Hiring Manager,",
                "introduction": "First paragraph introducing the candidate and position",
                "body": "Main paragraphs highlighting relevant experience and skills",
                "closing": "Closing paragraph with call to action",
                "signature": "Sincerely,\\n[Candidate Name]",
                "full_text": "The complete cover letter text"
            }
            """
            
            # Get cover letter from LLM
            response = self.client.generate_text(
                prompt=prompt,
                system_prompt=self.system_prompts["cover_letter"],
                max_tokens=2000,
                temperature=0.7,
            )
            
            try:
                # Parse JSON response
                cover_letter = json.loads(response)
                return cover_letter
            except json.JSONDecodeError:
                # Handle parsing error
                logger.error("Failed to parse LLM response as JSON")
                return {
                    "subject_line": "Application for [Job Title]",
                    "salutation": "Dear Hiring Manager,",
                    "introduction": "Could not generate introduction",
                    "body": "Could not generate body",
                    "closing": "Could not generate closing",
                    "signature": "Sincerely,\n[Candidate Name]",
                    "full_text": response
                }
        except Exception as e:
            logger.error(f"Error generating cover letter: {str(e)}")
            return {
                "status": "error",
                "message": f"Error generating cover letter: {str(e)}"
            }

    def tailor_resume(
        self,
        profile_data: Dict[str, Any],
        job_data: Dict[str, Any],
        customization_notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Tailor a resume for a job application using LLM.
        
        Args:
            profile_data: LinkedIn profile data
            job_data: Job data
            customization_notes: Additional notes for customization
            
        Returns:
            Dictionary with tailored resume recommendations
        """
        logger.info("Tailoring resume")
        
        try:
            # Create prompt for resume tailoring
            prompt = f"""
            Provide recommendations for tailoring a resume based on the following:
            
            Profile data:
            {json.dumps(profile_data, indent=2)}
            
            Job posting:
            {json.dumps(job_data, indent=2)}
            """
            
            if customization_notes:
                prompt += f"\n\nAdditional customization notes:\n{customization_notes}"
            
            prompt += """
            
            Provide:
            1. Keywords to include (important terms from the job posting)
            2. Skills to emphasize (skills that match the job requirements)
            3. Experiences to highlight (relevant experiences that should be featured)
            4. Achievements to showcase (quantifiable achievements that align with the job)
            5. Sections to add or remove
            
            Format your response as JSON with the following structure:
            {
                "keywords": ["keyword1", "keyword2", ...],
                "skills_to_emphasize": ["skill1", "skill2", ...],
                "experiences_to_highlight": [
                    {
                        "title": "Job Title",
                        "company": "Company Name",
                        "description": "How to present this experience"
                    },
                    ...
                ],
                "achievements_to_showcase": ["achievement1", "achievement2", ...],
                "sections": {
                    "add": ["section1", "section2", ...],
                    "remove": ["section1", "section2", ...],
                    "modify": [
                        {
                            "section": "section1",
                            "recommendation": "How to modify this section"
                        },
                        ...
                    ]
                },
                "general_recommendations": ["recommendation1", "recommendation2", ...]
            }
            """
            
            # Get resume recommendations from LLM
            response = self.client.generate_text(
                prompt=prompt,
                system_prompt=self.system_prompts["resume_tailoring"],
                max_tokens=2000,
                temperature=0.3,
            )
            
            try:
                # Parse JSON response
                resume_recommendations = json.loads(response)
                return resume_recommendations
            except json.JSONDecodeError:
                # Handle parsing error
                logger.error("Failed to parse LLM response as JSON")
                return {
                    "keywords": ["Could not parse keywords"],
                    "skills_to_emphasize": ["Could not parse skills"],
                    "experiences_to_highlight": [],
                    "achievements_to_showcase": ["Could not parse achievements"],
                    "sections": {
                        "add": [],
                        "remove": [],
                        "modify": []
                    },
                    "general_recommendations": ["Could not generate proper recommendations"],
                    "raw_response": response
                }
        except Exception as e:
            logger.error(f"Error tailoring resume: {str(e)}")
            return {
                "status": "error",
                "message": f"Error tailoring resume: {str(e)}"
            }

    def generate_message(
        self,
        sender_data: Dict[str, Any],
        recipient_data: Dict[str, Any],
        context: Dict[str, Any],
        message_type: str = "connection_request"
    ) -> Dict[str, Any]:
        """
        Generate a personalized message using LLM.
        
        Args:
            sender_data: Sender profile data
            recipient_data: Recipient profile data
            context: Additional context information
            message_type: Type of message (connection_request, follow_up, etc.)
            
        Returns:
            Dictionary with generated message
        """
        logger.info(f"Generating {message_type} message")
        
        try:
            # Create prompt for message generation
            prompt = f"""
            Generate a personalized {message_type} message based on the following:
            
            Sender profile:
            {json.dumps(sender_data, indent=2)}
            
            Recipient profile:
            {json.dumps(recipient_data, indent=2)}
            
            Context:
            {json.dumps(context, indent=2)}
            
            Format your response as JSON with the following structure:
            {{
                "subject": "Subject line (if applicable)",
                "message": "The complete message text",
                "follow_up": "Suggested follow-up message if no response"
            }}
            """
            
            # Get message from LLM
            response = self.client.generate_text(
                prompt=prompt,
                system_prompt=self.system_prompts["message_generation"],
                max_tokens=1000,
                temperature=0.7,
            )
            
            try:
                # Parse JSON response
                message = json.loads(response)
                return message
            except json.JSONDecodeError:
                # Handle parsing error
                logger.error("Failed to parse LLM response as JSON")
                return {
                    "subject": "",
                    "message": response,
                    "follow_up": ""
                }
        except Exception as e:
            logger.error(f"Error generating message: {str(e)}")
            return {
                "status": "error",
                "message": f"Error generating message: {str(e)}"
            }

    def prepare_interview(
        self,
        profile_data: Dict[str, Any],
        job_data: Dict[str, Any],
        interview_type: str = "behavioral"
    ) -> Dict[str, Any]:
        """
        Prepare interview materials using LLM.
        
        Args:
            profile_data: LinkedIn profile data
            job_data: Job data
            interview_type: Type of interview (behavioral, technical, case)
            
        Returns:
            Dictionary with interview preparation materials
        """
        logger.info(f"Preparing for {interview_type} interview")
        
        try:
            # Create prompt for interview preparation
            prompt = f"""
            Generate interview preparation materials for a {interview_type} interview based on the following:
            
            Profile data:
            {json.dumps(profile_data, indent=2)}
            
            Job posting:
            {json.dumps(job_data, indent=2)}
            
            Provide:
            1. Likely interview questions specific to this role and candidate
            2. Recommended answers that highlight the candidate's strengths
            3. Preparation tips tailored to this specific interview
            4. Questions the candidate should ask the interviewer
            
            Format your response as JSON with the following structure:
            {{
                "likely_questions": [
                    {{
                        "question": "Interview question",
                        "explanation": "Why this question might be asked",
                        "recommended_answer": "Suggested answer approach",
                        "key_points": ["point1", "point2", ...]
                    }},
                    ...
                ],
                "preparation_tips": ["tip1", "tip2", ...],
                "questions_to_ask": [
                    {{
                        "question": "Question to ask interviewer",
                        "purpose": "Why this question is strategic to ask"
                    }},
                    ...
                ],
                "general_advice": "Overall advice for this interview"
            }}
            """
            
            # Get interview preparation from LLM
            response = self.client.generate_text(
                prompt=prompt,
                system_prompt=self.system_prompts["interview_prep"],
                max_tokens=2500,
                temperature=0.4,
            )
            
            try:
                # Parse JSON response
                interview_prep = json.loads(response)
                return interview_prep
            except json.JSONDecodeError:
                # Handle parsing error
                logger.error("Failed to parse LLM response as JSON")
                return {
                    "likely_questions": [
                        {
                            "question": "Could not generate questions",
                            "explanation": "",
                            "recommended_answer": "",
                            "key_points": []
                        }
                    ],
                    "preparation_tips": ["Could not generate preparation tips"],
                    "questions_to_ask": [
                        {
                            "question": "Could not generate questions to ask",
                            "purpose": ""
                        }
                    ],
                    "general_advice": "Could not generate general advice",
                    "raw_response": response
                }
        except Exception as e:
            logger.error(f"Error preparing interview materials: {str(e)}")
            return {
                "status": "error",
                "message": f"Error preparing interview materials: {str(e)}"
            }


def get_llm_service(db: Session = None) -> LLMService:
    """
    Get an LLM service instance.
    
    Args:
        db: Database session
        
    Returns:
        LLM service instance
    """
    if db is None:
        db = SessionLocal()
    return LLMService(db=db) 