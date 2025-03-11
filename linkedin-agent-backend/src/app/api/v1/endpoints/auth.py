"""
Authentication endpoints for the LinkedIn AI Agent.
"""

from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.app.core.config import settings
from src.app.core.security import create_access_token, create_refresh_token
from src.app.db.session import get_db
from src.app.schemas.user import Token, User, UserCreate
# from src.app.services.user import authenticate_user, create_user, get_current_user

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    # Uncomment when user service is implemented
    # user = authenticate_user(db, form_data.username, form_data.password)
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Incorrect email or password",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    # if not user.is_active:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Inactive user",
    #     )
    
    # For now, return a placeholder token
    return {
        "access_token": "placeholder_access_token",
        "token_type": "bearer",
        "refresh_token": "placeholder_refresh_token",
    }


@router.post("/signup", response_model=User)
async def signup(
    user_in: UserCreate,
    db: Session = Depends(get_db),
) -> Any:
    """
    Create new user.
    """
    # Uncomment when user service is implemented
    # user = get_user_by_email(db, email=user_in.email)
    # if user:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Email already registered",
    #     )
    # user = create_user(db, user_in=user_in)
    
    # For now, return a placeholder user
    return {
        "id": "00000000-0000-0000-0000-000000000000",
        "email": user_in.email,
        "full_name": user_in.full_name,
        "is_active": True,
        "is_superuser": False,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00",
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(
    # token: str = Body(...),
    db: Session = Depends(get_db),
) -> Any:
    """
    Refresh token.
    """
    # Uncomment when token validation is implemented
    # try:
    #     payload = jwt.decode(
    #         token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
    #     )
    #     token_data = TokenPayload(**payload)
    # except (jwt.JWTError, ValidationError):
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Invalid token",
    #     )
    # user = get_user_by_id(db, id=token_data.sub)
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="User not found",
    #     )
    # if not user.is_active:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Inactive user",
    #     )
    
    # For now, return a placeholder token
    return {
        "access_token": "placeholder_access_token",
        "token_type": "bearer",
        "refresh_token": "placeholder_refresh_token",
    }


@router.post("/linkedin", response_model=Token)
async def login_linkedin(
    # linkedin_data: LinkedInOAuthRequest,
    db: Session = Depends(get_db),
) -> Any:
    """
    LinkedIn OAuth login.
    """
    # Uncomment when LinkedIn OAuth is implemented
    # try:
    #     linkedin_user = get_linkedin_user(linkedin_data.code, linkedin_data.redirect_uri)
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail=f"Could not validate LinkedIn credentials: {str(e)}",
    #     )
    # user = get_user_by_linkedin_id(db, linkedin_id=linkedin_user.id)
    # if not user:
    #     user = create_linkedin_user(db, linkedin_user=linkedin_user)
    
    # For now, return a placeholder token
    return {
        "access_token": "placeholder_access_token",
        "token_type": "bearer",
        "refresh_token": "placeholder_refresh_token",
    } 