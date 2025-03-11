"""
Job schemas for the LinkedIn AI Agent.
"""

import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field


# Job schemas
class JobBase(BaseModel):
    """Base job schema."""
    title: Optional[str] = None
    company: Optional[str] = None
    company_linkedin_id: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    job_url: Optional[str] = None
    employment_type: Optional[str] = None
    experience_level: Optional[str] = None
    industries: Optional[List[str]] = None
    functions: Optional[List[str]] = None
    required_skills: Optional[List[str]] = None
    preferred_skills: Optional[List[str]] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: Optional[str] = None
    is_remote: Optional[bool] = False
    posted_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None


class JobCreate(JobBase):
    """Job creation schema."""
    title: str
    company: str


class JobUpdate(JobBase):
    """Job update schema."""
    pass


class JobInDBBase(JobBase):
    """Base job in DB schema."""
    id: uuid.UUID
    linkedin_job_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True


class Job(JobInDBBase):
    """Job schema to return via API."""
    pass


class JobInDB(JobInDBBase):
    """Job in DB schema."""
    raw_data: Optional[Dict[str, Any]] = None


# Saved job schemas
class SavedJobBase(BaseModel):
    """Base saved job schema."""
    notes: Optional[str] = None


class SavedJobCreate(SavedJobBase):
    """Saved job creation schema."""
    user_id: uuid.UUID
    job_id: uuid.UUID


class SavedJobUpdate(SavedJobBase):
    """Saved job update schema."""
    pass


class SavedJobInDBBase(SavedJobBase):
    """Base saved job in DB schema."""
    id: uuid.UUID
    user_id: uuid.UUID
    job_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True


class SavedJob(SavedJobInDBBase):
    """Saved job schema to return via API."""
    job: Job


# Job match schemas
class JobMatchBase(BaseModel):
    """Base job match schema."""
    match_score: float
    match_analysis: Optional[str] = None
    skill_gaps: Optional[List[str]] = None


class JobMatchCreate(JobMatchBase):
    """Job match creation schema."""
    user_id: uuid.UUID
    job_id: uuid.UUID


class JobMatchUpdate(JobMatchBase):
    """Job match update schema."""
    pass


class JobMatchInDBBase(JobMatchBase):
    """Base job match in DB schema."""
    id: uuid.UUID
    user_id: uuid.UUID
    job_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True


class JobMatch(JobMatchInDBBase):
    """Job match schema to return via API."""
    job: Job 