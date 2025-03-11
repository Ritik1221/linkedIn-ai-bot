"""
Application model for the LinkedIn AI Agent.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text, JSON, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from src.app.db.session import Base


class ApplicationStatus(str, enum.Enum):
    """Application status enum."""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    VIEWED = "viewed"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    INTERVIEW_COMPLETED = "interview_completed"
    OFFER_RECEIVED = "offer_received"
    OFFER_ACCEPTED = "offer_accepted"
    OFFER_DECLINED = "offer_declined"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class Application(Base):
    """Job application model."""
    
    __tablename__ = "applications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id", ondelete="SET NULL"), nullable=True)
    cover_letter_id = Column(UUID(as_uuid=True), ForeignKey("cover_letters.id", ondelete="SET NULL"), nullable=True)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.DRAFT, nullable=False)
    application_date = Column(DateTime, nullable=True)
    linkedin_application_id = Column(String, unique=True, index=True, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
    job = relationship("Job", back_populates="applications")
    resume = relationship("Resume")
    cover_letter = relationship("CoverLetter")
    status_updates = relationship("ApplicationStatusUpdate", back_populates="application", cascade="all, delete-orphan")


class ApplicationStatusUpdate(Base):
    """Application status update model."""
    
    __tablename__ = "application_status_updates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = Column(UUID(as_uuid=True), ForeignKey("applications.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(ApplicationStatus), nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    application = relationship("Application", back_populates="status_updates")


class Resume(Base):
    """Resume model."""
    
    __tablename__ = "resumes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    file_url = Column(String, nullable=True)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User")


class CoverLetter(Base):
    """Cover letter model."""
    
    __tablename__ = "cover_letters"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=True)
    name = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    file_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
    job = relationship("Job") 