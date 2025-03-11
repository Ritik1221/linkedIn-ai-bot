"""
Authentication endpoints for the LinkedIn AI Agent.
"""

from datetime import timedelta, datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status, Body, Request
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from src.app.core.config import settings
from src.app.core.security import create_access_token, create_refresh_token
from src.app.core.linkedin_client import get_linkedin_client
from src.app.db.session import get_db
from src.app.schemas.user import Token, User, UserCreate, TokenPayload, LinkedInOAuthRequest
from src.app.services.user import (
    authenticate_user, 
    create_user, 
    get_user, 
    get_user_by_email, 
    get_user_by_linkedin_id,
    create_linkedin_user,
    update_user
)
from src.app.utils.rate_limit import rate_limit

router = APIRouter()

# Rate limiters for authentication endpoints
login_limit = rate_limit(times=5, seconds=300, prefix="rate_limit:login")
signup_limit = rate_limit(times=3, seconds=3600, prefix="rate_limit:signup")
refresh_limit = rate_limit(times=10, seconds=600, prefix="rate_limit:refresh")


@router.post("/login", response_model=Token)
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    _: bool = Depends(login_limit),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
        "refresh_token": create_refresh_token(
            user.id, expires_delta=refresh_token_expires
        ),
    }


@router.post("/signup", response_model=User)
async def signup(
    request: Request,
    user_in: UserCreate,
    db: Session = Depends(get_db),
    _: bool = Depends(signup_limit),
) -> Any:
    """
    Create new user.
    """
    user = get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    user = create_user(db, user_in=user_in)
    return user


@router.post("/refresh", response_model=Token)
async def refresh_token(
    request: Request,
    token: str = Body(...),
    db: Session = Depends(get_db),
    _: bool = Depends(refresh_limit),
) -> Any:
    """
    Refresh token.
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        # Check if token is a refresh token
        if getattr(token_data, "type", None) != "refresh":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token type",
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
        )
    
    user = get_user(db, user_id=token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
        "refresh_token": create_refresh_token(
            user.id, expires_delta=refresh_token_expires
        ),
    }


@router.post("/linkedin", response_model=Token)
async def login_linkedin(
    linkedin_data: LinkedInOAuthRequest,
    db: Session = Depends(get_db),
) -> Any:
    """
    LinkedIn OAuth login.
    """
    try:
        # Get LinkedIn client
        linkedin_client = get_linkedin_client()
        
        # Exchange code for access token
        token_data = linkedin_client.get_access_token(linkedin_data.code)
        
        # Get user profile from LinkedIn
        profile_data = linkedin_client.get_profile(token_data.get("access_token"))
        
        # Check if user exists
        user = get_user_by_linkedin_id(db, linkedin_id=profile_data.get("id"))
        
        if not user:
            # Create new user from LinkedIn data
            linkedin_user_data = {
                "id": profile_data.get("id"),
                "email": profile_data.get("email"),
                "name": f"{profile_data.get('firstName', '')} {profile_data.get('lastName', '')}".strip(),
                "access_token": token_data.get("access_token"),
                "refresh_token": token_data.get("refresh_token"),
                "expires_at": token_data.get("expires_at", 0)
            }
            user = create_linkedin_user(db, linkedin_user=linkedin_user_data)
        else:
            # Update existing user with new token
            update_user(db, user=user, user_in={
                "linkedin_access_token": token_data.get("access_token"),
                "linkedin_refresh_token": token_data.get("refresh_token", user.linkedin_refresh_token),
                "linkedin_token_expires_at": datetime.fromtimestamp(token_data.get("expires_at", 0))
            })
        
        # Create access and refresh tokens
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        
        return {
            "access_token": create_access_token(
                user.id, expires_delta=access_token_expires
            ),
            "token_type": "bearer",
            "refresh_token": create_refresh_token(
                user.id, expires_delta=refresh_token_expires
            ),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not validate LinkedIn credentials: {str(e)}",
        ) 