"""
User model for the LinkedIn AI Agent.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.app.db.session import Base

class User(Base):
    """User model."""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    linkedin_id = Column(String, unique=True, index=True, nullable=True)
    linkedin_access_token = Column(String, nullable=True)
    linkedin_refresh_token = Column(String, nullable=True)
    linkedin_token_expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan") 