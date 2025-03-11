"""
Profile endpoints for the LinkedIn AI Agent.
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.app.db.session import get_db
from src.app.schemas.profile import Profile, ProfileCreate, ProfileUpdate
# from src.app.services.profile import create_profile, get_profile, get_profiles, update_profile
# from src.app.services.user import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[Profile])
async def read_profiles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve profiles.
    """
    # Uncomment when profile service is implemented
    # profiles = get_profiles(db, skip=skip, limit=limit)
    
    # For now, return a placeholder list of profiles
    return [
        {
            "id": "00000000-0000-0000-0000-000000000000",
            "user_id": "00000000-0000-0000-0000-000000000000",
            "headline": "Software Engineer",
            "summary": "Experienced software engineer with a passion for building scalable applications.",
            "location": "San Francisco, CA",
            "industry": "Technology",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00",
        }
    ]


@router.post("/", response_model=Profile)
async def create_user_profile(
    profile_in: ProfileCreate,
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_active_user),
) -> Any:
    """
    Create new profile.
    """
    # Uncomment when profile service is implemented
    # profile = get_profile_by_user_id(db, user_id=current_user.id)
    # if profile:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Profile already exists for this user",
    #     )
    # profile = create_profile(db, profile_in=profile_in, user_id=current_user.id)
    
    # For now, return a placeholder profile
    return {
        "id": "00000000-0000-0000-0000-000000000000",
        "user_id": "00000000-0000-0000-0000-000000000000",
        "headline": profile_in.headline,
        "summary": profile_in.summary,
        "location": profile_in.location,
        "industry": profile_in.industry,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00",
    }


@router.get("/me", response_model=Profile)
async def read_user_profile(
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_active_user),
) -> Any:
    """
    Get current user profile.
    """
    # Uncomment when profile service is implemented
    # profile = get_profile_by_user_id(db, user_id=current_user.id)
    # if not profile:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Profile not found",
    #     )
    
    # For now, return a placeholder profile
    return {
        "id": "00000000-0000-0000-0000-000000000000",
        "user_id": "00000000-0000-0000-0000-000000000000",
        "headline": "Software Engineer",
        "summary": "Experienced software engineer with a passion for building scalable applications.",
        "location": "San Francisco, CA",
        "industry": "Technology",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00",
    }


@router.put("/me", response_model=Profile)
async def update_user_profile(
    profile_in: ProfileUpdate,
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_active_user),
) -> Any:
    """
    Update current user profile.
    """
    # Uncomment when profile service is implemented
    # profile = get_profile_by_user_id(db, user_id=current_user.id)
    # if not profile:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Profile not found",
    #     )
    # profile = update_profile(db, profile=profile, profile_in=profile_in)
    
    # For now, return a placeholder updated profile
    return {
        "id": "00000000-0000-0000-0000-000000000000",
        "user_id": "00000000-0000-0000-0000-000000000000",
        "headline": profile_in.headline or "Software Engineer",
        "summary": profile_in.summary or "Experienced software engineer with a passion for building scalable applications.",
        "location": profile_in.location or "San Francisco, CA",
        "industry": profile_in.industry or "Technology",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00",
    }


@router.get("/{profile_id}", response_model=Profile)
async def read_profile(
    profile_id: str,
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_active_user),
) -> Any:
    """
    Get profile by ID.
    """
    # Uncomment when profile service is implemented
    # profile = get_profile(db, id=profile_id)
    # if not profile:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Profile not found",
    #     )
    
    # For now, return a placeholder profile
    return {
        "id": profile_id,
        "user_id": "00000000-0000-0000-0000-000000000000",
        "headline": "Software Engineer",
        "summary": "Experienced software engineer with a passion for building scalable applications.",
        "location": "San Francisco, CA",
        "industry": "Technology",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00",
    } 