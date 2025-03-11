"""
Profile service for the LinkedIn AI Agent.
This module provides functions for profile management and LinkedIn profile synchronization.
"""

from typing import Any, Dict, List, Optional, Union

from sqlalchemy.orm import Session

from src.app.models.profile import Profile
from src.app.models.user import User
from src.app.schemas.profile import ProfileCreate, ProfileUpdate


def get_profile(db: Session, profile_id: str) -> Optional[Profile]:
    """
    Get a profile by ID.
    
    Args:
        db: Database session
        profile_id: Profile ID
        
    Returns:
        Profile object if found, None otherwise
    """
    return db.query(Profile).filter(Profile.id == profile_id).first()


def get_profile_by_user_id(db: Session, user_id: str) -> Optional[Profile]:
    """
    Get a profile by user ID.
    
    Args:
        db: Database session
        user_id: User ID
        
    Returns:
        Profile object if found, None otherwise
    """
    return db.query(Profile).filter(Profile.user_id == user_id).first()


def get_profiles(
    db: Session, skip: int = 0, limit: int = 100
) -> List[Profile]:
    """
    Get multiple profiles with pagination.
    
    Args:
        db: Database session
        skip: Number of profiles to skip
        limit: Maximum number of profiles to return
        
    Returns:
        List of profile objects
    """
    return db.query(Profile).offset(skip).limit(limit).all()


def create_profile(
    db: Session, profile_in: ProfileCreate, user_id: str
) -> Profile:
    """
    Create a new profile.
    
    Args:
        db: Database session
        profile_in: Profile creation data
        user_id: User ID
        
    Returns:
        Created profile object
    """
    profile_data = profile_in.model_dump()
    db_profile = Profile(**profile_data, user_id=user_id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def update_profile(
    db: Session, profile: Profile, profile_in: Union[ProfileUpdate, Dict[str, Any]]
) -> Profile:
    """
    Update a profile.
    
    Args:
        db: Database session
        profile: Profile object to update
        profile_in: Profile update data
        
    Returns:
        Updated profile object
    """
    profile_data = profile.__dict__
    if isinstance(profile_in, dict):
        update_data = profile_in
    else:
        update_data = profile_in.model_dump(exclude_unset=True)
    
    for field in profile_data:
        if field in update_data:
            setattr(profile, field, update_data[field])
    
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def delete_profile(db: Session, profile_id: str) -> Profile:
    """
    Delete a profile.
    
    Args:
        db: Database session
        profile_id: Profile ID
        
    Returns:
        Deleted profile object
    """
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    db.delete(profile)
    db.commit()
    return profile


def sync_linkedin_profile(db: Session, user: User, linkedin_data: Dict[str, Any]) -> Profile:
    """
    Synchronize a user's profile with LinkedIn data.
    
    Args:
        db: Database session
        user: User object
        linkedin_data: LinkedIn profile data
        
    Returns:
        Updated profile object
    """
    profile = get_profile_by_user_id(db, user_id=str(user.id))
    
    # Map LinkedIn data to profile fields
    profile_data = {
        "headline": linkedin_data.get("headline"),
        "summary": linkedin_data.get("summary"),
        "industry": linkedin_data.get("industry"),
        "location": linkedin_data.get("location", {}).get("name"),
        "profile_picture_url": linkedin_data.get("profilePicture", {}).get("displayImage"),
    }
    
    # Handle education
    if "education" in linkedin_data:
        education_list = []
        for edu in linkedin_data["education"]:
            education_list.append({
                "school": edu.get("schoolName"),
                "degree": edu.get("degreeName"),
                "field_of_study": edu.get("fieldOfStudy"),
                "start_date": f"{edu.get('startDate', {}).get('year')}-{edu.get('startDate', {}).get('month', 1):02d}-01" if edu.get("startDate") else None,
                "end_date": f"{edu.get('endDate', {}).get('year')}-{edu.get('endDate', {}).get('month', 1):02d}-01" if edu.get("endDate") else None,
                "description": edu.get("description"),
            })
        profile_data["education"] = education_list
    
    # Handle experience
    if "positions" in linkedin_data:
        experience_list = []
        for pos in linkedin_data["positions"]:
            experience_list.append({
                "title": pos.get("title"),
                "company": pos.get("companyName"),
                "location": pos.get("location"),
                "start_date": f"{pos.get('startDate', {}).get('year')}-{pos.get('startDate', {}).get('month', 1):02d}-01" if pos.get("startDate") else None,
                "end_date": f"{pos.get('endDate', {}).get('year')}-{pos.get('endDate', {}).get('month', 1):02d}-01" if pos.get("endDate") else None,
                "description": pos.get("description"),
            })
        profile_data["experience"] = experience_list
    
    # Handle skills
    if "skills" in linkedin_data:
        skills_list = []
        for skill in linkedin_data["skills"]:
            skills_list.append({
                "name": skill.get("name"),
                "endorsement_count": skill.get("endorsementCount", 0),
            })
        profile_data["skills"] = skills_list
    
    # Update or create profile
    if profile:
        return update_profile(db, profile=profile, profile_in=profile_data)
    else:
        return create_profile(db, profile_in=ProfileCreate(**profile_data), user_id=str(user.id))


def analyze_profile_strength(profile: Profile) -> Dict[str, Any]:
    """
    Analyze the strength of a profile.
    
    Args:
        profile: Profile object
        
    Returns:
        Profile strength analysis
    """
    # This is a placeholder for the LLM-based profile analysis
    # In a real implementation, this would call the LLM service
    
    # Calculate basic completeness score
    completeness_score = 0
    total_fields = 0
    
    # Check basic fields
    for field in ["headline", "summary", "industry", "location"]:
        total_fields += 1
        if getattr(profile, field):
            completeness_score += 1
    
    # Check education
    total_fields += 1
    if profile.education and len(profile.education) > 0:
        completeness_score += 1
    
    # Check experience
    total_fields += 1
    if profile.experience and len(profile.experience) > 0:
        completeness_score += 1
    
    # Check skills
    total_fields += 1
    if profile.skills and len(profile.skills) > 0:
        completeness_score += 1
    
    # Calculate percentage
    completeness_percentage = (completeness_score / total_fields) * 100 if total_fields > 0 else 0
    
    return {
        "completeness_score": completeness_percentage,
        "missing_fields": [
            field for field in ["headline", "summary", "industry", "location"] 
            if not getattr(profile, field)
        ],
        "has_education": bool(profile.education and len(profile.education) > 0),
        "has_experience": bool(profile.experience and len(profile.experience) > 0),
        "has_skills": bool(profile.skills and len(profile.skills) > 0),
        "recommendations": [
            "Add a compelling headline that showcases your value proposition" if not profile.headline else None,
            "Write a comprehensive summary that highlights your achievements and aspirations" if not profile.summary else None,
            "Add your industry to help with job matching" if not profile.industry else None,
            "Include your location to improve job recommendations" if not profile.location else None,
            "Add your educational background" if not (profile.education and len(profile.education) > 0) else None,
            "Include your work experience" if not (profile.experience and len(profile.experience) > 0) else None,
            "Add relevant skills to your profile" if not (profile.skills and len(profile.skills) > 0) else None,
        ],
    }


def identify_skills_gap(profile: Profile, job_requirements: List[str]) -> Dict[str, Any]:
    """
    Identify skills gap between a profile and job requirements.
    
    Args:
        profile: Profile object
        job_requirements: List of required skills for a job
        
    Returns:
        Skills gap analysis
    """
    # This is a placeholder for the LLM-based skills gap analysis
    # In a real implementation, this would call the LLM service
    
    # Extract profile skills
    profile_skills = []
    if profile.skills:
        profile_skills = [skill["name"].lower() for skill in profile.skills]
    
    # Compare with job requirements
    missing_skills = []
    matching_skills = []
    
    for skill in job_requirements:
        skill_lower = skill.lower()
        if skill_lower in profile_skills:
            matching_skills.append(skill)
        else:
            missing_skills.append(skill)
    
    # Calculate match percentage
    match_percentage = (len(matching_skills) / len(job_requirements)) * 100 if job_requirements else 0
    
    return {
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "match_percentage": match_percentage,
        "recommendations": [
            f"Consider developing skills in {skill}" for skill in missing_skills
        ],
    }


def generate_improvement_recommendations(profile: Profile) -> List[str]:
    """
    Generate recommendations for profile improvement.
    
    Args:
        profile: Profile object
        
    Returns:
        List of improvement recommendations
    """
    # This is a placeholder for the LLM-based recommendation generation
    # In a real implementation, this would call the LLM service
    
    recommendations = []
    
    # Check headline
    if not profile.headline or len(profile.headline) < 10:
        recommendations.append("Create a compelling headline that showcases your expertise and value proposition.")
    
    # Check summary
    if not profile.summary or len(profile.summary) < 100:
        recommendations.append("Write a comprehensive summary that highlights your achievements, skills, and career aspirations.")
    
    # Check experience
    if not profile.experience or len(profile.experience) == 0:
        recommendations.append("Add your work experience with detailed descriptions of your responsibilities and achievements.")
    else:
        for exp in profile.experience:
            if not exp.get("description") or len(exp.get("description", "")) < 50:
                recommendations.append(f"Enhance your description for the {exp.get('title')} role at {exp.get('company')} with specific achievements and metrics.")
    
    # Check education
    if not profile.education or len(profile.education) == 0:
        recommendations.append("Add your educational background to strengthen your profile.")
    
    # Check skills
    if not profile.skills or len(profile.skills) < 5:
        recommendations.append("Add more relevant skills to your profile to improve visibility in job searches.")
    
    # General recommendations
    recommendations.extend([
        "Request recommendations from colleagues and supervisors to build credibility.",
        "Join relevant LinkedIn groups to expand your network and demonstrate industry engagement.",
        "Regularly share industry content and insights to establish thought leadership.",
        "Ensure your profile picture is professional and approachable.",
    ])
    
    return recommendations 