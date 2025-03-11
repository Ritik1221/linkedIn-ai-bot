"""
User schemas for the LinkedIn AI Agent.
"""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# Shared properties
class UserBase(BaseModel):
    """Base user schema."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    """User creation schema."""
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    """User update schema."""
    password: Optional[str] = None


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    """Base user in DB schema."""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True


# Properties to return via API
class User(UserInDBBase):
    """User schema to return via API."""
    pass


# Properties stored in DB
class UserInDB(UserInDBBase):
    """User in DB schema."""
    hashed_password: str


# Token schemas
class Token(BaseModel):
    """Token schema."""
    access_token: str
    token_type: str = "bearer"
    refresh_token: str


class TokenPayload(BaseModel):
    """Token payload schema."""
    sub: str
    exp: int


# LinkedIn OAuth schemas
class LinkedInOAuthRequest(BaseModel):
    """LinkedIn OAuth request schema."""
    code: str
    redirect_uri: str


class LinkedInOAuthResponse(BaseModel):
    """LinkedIn OAuth response schema."""
    access_token: str
    token_type: str = "bearer"
    refresh_token: str
    user: User 