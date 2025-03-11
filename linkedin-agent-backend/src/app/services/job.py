"""
Job service for the LinkedIn AI Agent.
This module provides functions for job management, search, filtering, and recommendations.
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union

from sqlalchemy import and_, or_, desc, func
from sqlalchemy.orm import Session

from src.app.models.job import Job
from src.app.models.profile import Profile
from src.app.schemas.job import JobCreate, JobUpdate


def get_job(db: Session, job_id: str) -> Optional[Job]:
    """
    Get a job by ID.
    
    Args:
        db: Database session
        job_id: Job ID
        
    Returns:
        Job object if found, None otherwise
    """
    return db.query(Job).filter(Job.id == job_id).first()


def get_jobs(
    db: Session, skip: int = 0, limit: int = 100
) -> List[Job]:
    """
    Get multiple jobs with pagination.
    
    Args:
        db: Database session
        skip: Number of jobs to skip
        limit: Maximum number of jobs to return
        
    Returns:
        List of job objects
    """
    return db.query(Job).offset(skip).limit(limit).all()


def create_job(
    db: Session, job_in: JobCreate
) -> Job:
    """
    Create a new job.
    
    Args:
        db: Database session
        job_in: Job creation data
        
    Returns:
        Created job object
    """
    job_data = job_in.model_dump()
    db_job = Job(**job_data)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def update_job(
    db: Session, job: Job, job_in: Union[JobUpdate, Dict[str, Any]]
) -> Job:
    """
    Update a job.
    
    Args:
        db: Database session
        job: Job object to update
        job_in: Job update data
        
    Returns:
        Updated job object
    """
    job_data = job.__dict__
    if isinstance(job_in, dict):
        update_data = job_in
    else:
        update_data = job_in.model_dump(exclude_unset=True)
    
    for field in job_data:
        if field in update_data:
            setattr(job, field, update_data[field])
    
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def delete_job(db: Session, job_id: str) -> Job:
    """
    Delete a job.
    
    Args:
        db: Database session
        job_id: Job ID
        
    Returns:
        Deleted job object
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    db.delete(job)
    db.commit()
    return job


def search_jobs(
    db: Session,
    query: Optional[str] = None,
    location: Optional[str] = None,
    company: Optional[str] = None,
    job_type: Optional[str] = None,
    experience_level: Optional[str] = None,
    posted_within_days: Optional[int] = None,
    skills: Optional[List[str]] = None,
    skip: int = 0,
    limit: int = 100,
) -> List[Job]:
    """
    Search for jobs with various filters.
    
    Args:
        db: Database session
        query: Search query for title and description
        location: Job location
        company: Company name
        job_type: Job type (e.g., full-time, part-time)
        experience_level: Experience level
        posted_within_days: Jobs posted within the specified number of days
        skills: Required skills
        skip: Number of jobs to skip
        limit: Maximum number of jobs to return
        
    Returns:
        List of job objects matching the search criteria
    """
    jobs_query = db.query(Job)
    
    # Apply filters
    if query:
        jobs_query = jobs_query.filter(
            or_(
                Job.title.ilike(f"%{query}%"),
                Job.description.ilike(f"%{query}%"),
            )
        )
    
    if location:
        jobs_query = jobs_query.filter(Job.location.ilike(f"%{location}%"))
    
    if company:
        jobs_query = jobs_query.filter(Job.company.ilike(f"%{company}%"))
    
    if job_type:
        jobs_query = jobs_query.filter(Job.job_type == job_type)
    
    if experience_level:
        jobs_query = jobs_query.filter(Job.experience_level == experience_level)
    
    if posted_within_days:
        cutoff_date = datetime.utcnow() - timedelta(days=posted_within_days)
        jobs_query = jobs_query.filter(Job.posted_at >= cutoff_date)
    
    if skills and len(skills) > 0:
        # This assumes skills are stored as a JSONB array in the database
        # Adjust based on your actual database schema
        for skill in skills:
            jobs_query = jobs_query.filter(Job.required_skills.contains([skill]))
    
    # Order by most recent first
    jobs_query = jobs_query.order_by(desc(Job.posted_at))
    
    # Apply pagination
    jobs = jobs_query.offset(skip).limit(limit).all()
    
    return jobs


def recommend_jobs_for_profile(
    db: Session, profile: Profile, limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Recommend jobs for a user profile based on skills and experience.
    
    Args:
        db: Database session
        profile: User profile
        limit: Maximum number of jobs to recommend
        
    Returns:
        List of recommended jobs with match scores
    """
    # Extract profile skills
    profile_skills = []
    if profile.skills:
        profile_skills = [skill["name"].lower() for skill in profile.skills]
    
    # Extract profile industry
    profile_industry = profile.industry.lower() if profile.industry else ""
    
    # Extract profile location
    profile_location = profile.location.lower() if profile.location else ""
    
    # Get all jobs
    jobs = db.query(Job).all()
    
    # Calculate match scores
    job_matches = []
    for job in jobs:
        match_score = 0
        match_reasons = []
        
        # Skills match (highest weight)
        if job.required_skills:
            job_skills = [skill.lower() for skill in job.required_skills]
            matching_skills = [skill for skill in profile_skills if skill in job_skills]
            skill_match_percentage = len(matching_skills) / len(job_skills) if job_skills else 0
            match_score += skill_match_percentage * 0.5  # 50% weight for skills
            
            if matching_skills:
                match_reasons.append(f"You have {len(matching_skills)} of {len(job_skills)} required skills")
        
        # Industry match
        if profile_industry and job.industry and profile_industry in job.industry.lower():
            match_score += 0.2  # 20% weight for industry
            match_reasons.append("Industry match")
        
        # Location match
        if profile_location and job.location and profile_location in job.location.lower():
            match_score += 0.2  # 20% weight for location
            match_reasons.append("Location match")
        
        # Experience level match
        if profile.experience and job.experience_level:
            # Simple heuristic: count years of experience
            years_of_experience = 0
            for exp in profile.experience:
                start_date = exp.get("start_date")
                end_date = exp.get("end_date") or datetime.now().strftime("%Y-%m-%d")
                
                if start_date:
                    start_year = int(start_date.split("-")[0])
                    end_year = int(end_date.split("-")[0])
                    years_of_experience += end_year - start_year
            
            # Match experience level
            if job.experience_level == "entry" and years_of_experience <= 2:
                match_score += 0.1  # 10% weight for experience level
                match_reasons.append("Experience level match")
            elif job.experience_level == "mid" and 2 < years_of_experience <= 5:
                match_score += 0.1
                match_reasons.append("Experience level match")
            elif job.experience_level == "senior" and years_of_experience > 5:
                match_score += 0.1
                match_reasons.append("Experience level match")
        
        # Add to results if there's any match
        if match_score > 0:
            job_matches.append({
                "job": job,
                "match_score": match_score,
                "match_percentage": int(match_score * 100),
                "match_reasons": match_reasons
            })
    
    # Sort by match score (descending)
    job_matches.sort(key=lambda x: x["match_score"], reverse=True)
    
    # Return top matches
    return job_matches[:limit]


def get_trending_jobs(db: Session, limit: int = 10) -> List[Job]:
    """
    Get trending jobs based on recent postings and popularity.
    
    Args:
        db: Database session
        limit: Maximum number of jobs to return
        
    Returns:
        List of trending job objects
    """
    # Get jobs posted in the last 30 days
    cutoff_date = datetime.utcnow() - timedelta(days=30)
    recent_jobs = db.query(Job).filter(Job.posted_at >= cutoff_date)
    
    # Order by a combination of recency and views (if available)
    # This is a simplified version - in a real implementation, you might
    # want to use a more sophisticated algorithm
    trending_jobs = recent_jobs.order_by(desc(Job.posted_at)).limit(limit).all()
    
    return trending_jobs 