"""
Application schemas for the LinkedIn AI Agent.
"""

import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field

from src.app.models.application import ApplicationStatus
from src.app.schemas.job import Job


# Resume schemas
class ResumeBase(BaseModel):
    """Base resume schema."""
    name: Optional[str] = None
    content: Optional[str] = None
    file_url: Optional[str] = None
    is_default: Optional[bool] = False


class ResumeCreate(ResumeBase):
    """Resume creation schema."""
    name: str
    content: str
    user_id: uuid.UUID


class ResumeUpdate(ResumeBase):
    """Resume update schema."""
    pass


class ResumeInDBBase(ResumeBase):
    """Base resume in DB schema."""
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True


class Resume(ResumeInDBBase):
    """Resume schema to return via API."""
    pass


# Cover letter schemas
class CoverLetterBase(BaseModel):
    """Base cover letter schema."""
    name: Optional[str] = None
    content: Optional[str] = None
    file_url: Optional[str] = None


class CoverLetterCreate(CoverLetterBase):
    """Cover letter creation schema."""
    name: str
    content: str
    user_id: uuid.UUID
    job_id: Optional[uuid.UUID] = None


class CoverLetterUpdate(CoverLetterBase):
    """Cover letter update schema."""
    pass


class CoverLetterInDBBase(CoverLetterBase):
    """Base cover letter in DB schema."""
    id: uuid.UUID
    user_id: uuid.UUID
    job_id: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True


class CoverLetter(CoverLetterInDBBase):
    """Cover letter schema to return via API."""
    pass


# Application status update schemas
class ApplicationStatusUpdateBase(BaseModel):
    """Base application status update schema."""
    status: ApplicationStatus
    notes: Optional[str] = None


class ApplicationStatusUpdateCreate(ApplicationStatusUpdateBase):
    """Application status update creation schema."""
    application_id: uuid.UUID


class ApplicationStatusUpdateInDBBase(ApplicationStatusUpdateBase):
    """Base application status update in DB schema."""
    id: uuid.UUID
    application_id: uuid.UUID
    created_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True


class ApplicationStatusUpdate(ApplicationStatusUpdateInDBBase):
    """Application status update schema to return via API."""
    pass


# Application schemas
class ApplicationBase(BaseModel):
    """Base application schema."""
    status: Optional[ApplicationStatus] = ApplicationStatus.DRAFT
    application_date: Optional[datetime] = None
    linkedin_application_id: Optional[str] = None
    notes: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    """Application creation schema."""
    user_id: uuid.UUID
    job_id: uuid.UUID
    resume_id: Optional[uuid.UUID] = None
    cover_letter_id: Optional[uuid.UUID] = None


class ApplicationUpdate(ApplicationBase):
    """Application update schema."""
    resume_id: Optional[uuid.UUID] = None
    cover_letter_id: Optional[uuid.UUID] = None


class ApplicationInDBBase(ApplicationBase):
    """Base application in DB schema."""
    id: uuid.UUID
    user_id: uuid.UUID
    job_id: uuid.UUID
    resume_id: Optional[uuid.UUID] = None
    cover_letter_id: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True


class Application(ApplicationInDBBase):
    """Application schema to return via API."""
    job: Job
    resume: Optional[Resume] = None
    cover_letter: Optional[CoverLetter] = None
    status_updates: List[ApplicationStatusUpdate] = [] 