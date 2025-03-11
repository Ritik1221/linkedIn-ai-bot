"""
Profile schemas for the LinkedIn AI Agent.
"""

import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field


# Experience schemas
class ExperienceBase(BaseModel):
    """Base experience schema."""
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_current: Optional[bool] = False


class ExperienceCreate(ExperienceBase):
    """Experience creation schema."""
    title: str
    company: str


class ExperienceUpdate(ExperienceBase):
    """Experience update schema."""
    pass


class ExperienceInDBBase(ExperienceBase):
    """Base experience in DB schema."""
    id: uuid.UUID
    profile_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True


class Experience(ExperienceInDBBase):
    """Experience schema to return via API."""
    pass


# Education schemas
class EducationBase(BaseModel):
    """Base education schema."""
    school: Optional[str] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class EducationCreate(EducationBase):
    """Education creation schema."""
    school: str


class EducationUpdate(EducationBase):
    """Education update schema."""
    pass


class EducationInDBBase(EducationBase):
    """Base education in DB schema."""
    id: uuid.UUID
    profile_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True


class Education(EducationInDBBase):
    """Education schema to return via API."""
    pass


# Certification schemas
class CertificationBase(BaseModel):
    """Base certification schema."""
    name: Optional[str] = None
    issuing_organization: Optional[str] = None
    issue_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None


class CertificationCreate(CertificationBase):
    """Certification creation schema."""
    name: str
    issuing_organization: str


class CertificationUpdate(CertificationBase):
    """Certification update schema."""
    pass


class CertificationInDBBase(CertificationBase):
    """Base certification in DB schema."""
    id: uuid.UUID
    profile_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True


class Certification(CertificationInDBBase):
    """Certification schema to return via API."""
    pass


# Profile schemas
class ProfileBase(BaseModel):
    """Base profile schema."""
    headline: Optional[str] = None
    summary: Optional[str] = None
    industry: Optional[str] = None
    location: Optional[str] = None
    profile_picture_url: Optional[str] = None
    public_profile_url: Optional[str] = None
    skills: Optional[List[str]] = None


class ProfileCreate(ProfileBase):
    """Profile creation schema."""
    user_id: uuid.UUID


class ProfileUpdate(ProfileBase):
    """Profile update schema."""
    pass


class ProfileInDBBase(ProfileBase):
    """Base profile in DB schema."""
    id: uuid.UUID
    user_id: uuid.UUID
    last_synced_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True


class Profile(ProfileInDBBase):
    """Profile schema to return via API."""
    experiences: List[Experience] = []
    educations: List[Education] = []
    certifications: List[Certification] = []


class ProfileInDB(ProfileInDBBase):
    """Profile in DB schema."""
    raw_data: Optional[Dict[str, Any]] = None 