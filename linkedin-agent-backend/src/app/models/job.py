"""
Job model for the LinkedIn AI Agent.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text, JSON, Integer, Float
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship

from src.app.db.session import Base

class Job(Base):
    """LinkedIn job model."""
    
    __tablename__ = "jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    linkedin_job_id = Column(String, unique=True, index=True, nullable=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    company_linkedin_id = Column(String, nullable=True)
    location = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    job_url = Column(String, nullable=True)
    employment_type = Column(String, nullable=True)
    experience_level = Column(String, nullable=True)
    industries = Column(ARRAY(String), nullable=True)
    functions = Column(ARRAY(String), nullable=True)
    required_skills = Column(ARRAY(String), nullable=True)
    preferred_skills = Column(ARRAY(String), nullable=True)
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    salary_currency = Column(String, nullable=True)
    is_remote = Column(Boolean, default=False)
    posted_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    raw_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    saved_by_users = relationship("SavedJob", back_populates="job", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")
    matches = relationship("JobMatch", back_populates="job", cascade="all, delete-orphan")


class SavedJob(Base):
    """Saved job model."""
    
    __tablename__ = "saved_jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
    job = relationship("Job", back_populates="saved_by_users")


class JobMatch(Base):
    """Job match model."""
    
    __tablename__ = "job_matches"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    match_score = Column(Float, nullable=False)
    match_analysis = Column(Text, nullable=True)
    skill_gaps = Column(ARRAY(String), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
    job = relationship("Job", back_populates="matches") 