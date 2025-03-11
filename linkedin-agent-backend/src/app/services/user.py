"""
User service for the LinkedIn AI Agent.
This module provides functions for user authentication, creation, and management.
"""

from datetime import datetime
from typing import Any, Dict, Optional, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from src.app.core.config import settings
from src.app.core.security import get_password_hash, verify_password
from src.app.db.session import get_db
from src.app.models.user import User
from src.app.schemas.user import TokenPayload, UserCreate, UserUpdate

# OAuth2 token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def get_user(db: Session, user_id: str) -> Optional[User]:
    """
    Get a user by ID.
    
    Args:
        db: Database session
        user_id: User ID
        
    Returns:
        User object if found, None otherwise
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Get a user by email.
    
    Args:
        db: Database session
        email: User email
        
    Returns:
        User object if found, None otherwise
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_linkedin_id(db: Session, linkedin_id: str) -> Optional[User]:
    """
    Get a user by LinkedIn ID.
    
    Args:
        db: Database session
        linkedin_id: LinkedIn user ID
        
    Returns:
        User object if found, None otherwise
    """
    return db.query(User).filter(User.linkedin_id == linkedin_id).first()


def create_user(db: Session, user_in: UserCreate) -> User:
    """
    Create a new user.
    
    Args:
        db: Database session
        user_in: User creation data
        
    Returns:
        Created user object
    """
    db_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        is_active=user_in.is_active,
        is_superuser=user_in.is_superuser,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_linkedin_user(db: Session, linkedin_user: Dict[str, Any]) -> User:
    """
    Create a new user from LinkedIn data.
    
    Args:
        db: Database session
        linkedin_user: LinkedIn user data
        
    Returns:
        Created user object
    """
    db_user = User(
        email=linkedin_user.get("email"),
        full_name=linkedin_user.get("name"),
        linkedin_id=linkedin_user.get("id"),
        linkedin_access_token=linkedin_user.get("access_token"),
        linkedin_refresh_token=linkedin_user.get("refresh_token"),
        linkedin_token_expires_at=datetime.fromtimestamp(linkedin_user.get("expires_at", 0)),
        is_active=True,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(
    db: Session, user: User, user_in: Union[UserUpdate, Dict[str, Any]]
) -> User:
    """
    Update a user.
    
    Args:
        db: Database session
        user: User object to update
        user_in: User update data
        
    Returns:
        Updated user object
    """
    user_data = user.__dict__
    if isinstance(user_in, dict):
        update_data = user_in
    else:
        update_data = user_in.model_dump(exclude_unset=True)
    
    if update_data.get("password"):
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password
    
    for field in user_data:
        if field in update_data:
            setattr(user, field, update_data[field])
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user.
    
    Args:
        db: Database session
        email: User email
        password: User password
        
    Returns:
        User object if authentication successful, None otherwise
    """
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """
    Get the current authenticated user.
    
    Args:
        db: Database session
        token: JWT token
        
    Returns:
        Current user object
        
    Raises:
        HTTPException: If authentication fails
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        # Check if token is expired
        if datetime.fromtimestamp(token_data.exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = get_user(db, user_id=token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Get the current active user.
    
    Args:
        current_user: Current user object
        
    Returns:
        Current active user object
        
    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return current_user


def get_current_active_superuser(current_user: User = Depends(get_current_user)) -> User:
    """
    Get the current active superuser.
    
    Args:
        current_user: Current user object
        
    Returns:
        Current active superuser object
        
    Raises:
        HTTPException: If user is not a superuser
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return current_user 