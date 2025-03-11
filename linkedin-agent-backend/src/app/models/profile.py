"""
Profile model for the LinkedIn AI Agent.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship

from src.app.db.session import Base

class Profile(Base):
    """LinkedIn profile model."""
    
    __tablename__ = "profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    linkedin_profile_id = Column(String, unique=True, index=True, nullable=True)
    headline = Column(String, nullable=True)
    summary = Column(Text, nullable=True)
    industry = Column(String, nullable=True)
    location = Column(String, nullable=True)
    profile_picture_url = Column(String, nullable=True)
    public_profile_url = Column(String, nullable=True)
    skills = Column(ARRAY(String), nullable=True)
    raw_data = Column(JSON, nullable=True)
    last_synced_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="profile")
    experiences = relationship("Experience", back_populates="profile", cascade="all, delete-orphan")
    educations = relationship("Education", back_populates="profile", cascade="all, delete-orphan")
    certifications = relationship("Certification", back_populates="profile", cascade="all, delete-orphan")


class Experience(Base):
    """LinkedIn experience model."""
    
    __tablename__ = "experiences"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    linkedin_experience_id = Column(String, unique=True, index=True, nullable=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    is_current = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    profile = relationship("Profile", back_populates="experiences")


class Education(Base):
    """LinkedIn education model."""
    
    __tablename__ = "educations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    linkedin_education_id = Column(String, unique=True, index=True, nullable=True)
    school = Column(String, nullable=False)
    degree = Column(String, nullable=True)
    field_of_study = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    profile = relationship("Profile", back_populates="educations")


class Certification(Base):
    """LinkedIn certification model."""
    
    __tablename__ = "certifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    linkedin_certification_id = Column(String, unique=True, index=True, nullable=True)
    name = Column(String, nullable=False)
    issuing_organization = Column(String, nullable=False)
    issue_date = Column(DateTime, nullable=True)
    expiration_date = Column(DateTime, nullable=True)
    credential_id = Column(String, nullable=True)
    credential_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    profile = relationship("Profile", back_populates="certifications") 