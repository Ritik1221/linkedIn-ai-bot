"""
Profile endpoints for the LinkedIn AI Agent.
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.app.db.session import get_db
from src.app.models.user import User
from src.app.schemas.profile import Profile, ProfileCreate, ProfileUpdate
from src.app.services.profile import (
    create_profile, 
    get_profile, 
    get_profile_by_user_id,
    get_profiles, 
    update_profile,
    analyze_profile_strength,
    identify_skills_gap,
    generate_improvement_recommendations
)
from src.app.services.user import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[Profile])
async def read_profiles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve profiles.
    """
    profiles = get_profiles(db, skip=skip, limit=limit)
    return profiles


@router.post("/", response_model=Profile)
async def create_user_profile(
    profile_in: ProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new profile.
    """
    profile = get_profile_by_user_id(db, user_id=str(current_user.id))
    if profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists for this user",
        )
    profile = create_profile(db, profile_in=profile_in, user_id=str(current_user.id))
    return profile


@router.get("/me", response_model=Profile)
async def read_user_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user profile.
    """
    profile = get_profile_by_user_id(db, user_id=str(current_user.id))
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )
    return profile


@router.put("/me", response_model=Profile)
async def update_user_profile(
    profile_in: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update current user profile.
    """
    profile = get_profile_by_user_id(db, user_id=str(current_user.id))
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )
    profile = update_profile(db, profile=profile, profile_in=profile_in)
    return profile


@router.get("/me/analyze", response_model=dict)
async def analyze_user_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Analyze current user profile strength.
    """
    profile = get_profile_by_user_id(db, user_id=str(current_user.id))
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )
    analysis = analyze_profile_strength(profile)
    return analysis


@router.post("/me/skills-gap", response_model=dict)
async def analyze_skills_gap(
    job_requirements: List[str],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Analyze skills gap between user profile and job requirements.
    """
    profile = get_profile_by_user_id(db, user_id=str(current_user.id))
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )
    gap_analysis = identify_skills_gap(profile, job_requirements)
    return gap_analysis


@router.get("/me/recommendations", response_model=List[str])
async def get_profile_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get recommendations for profile improvement.
    """
    profile = get_profile_by_user_id(db, user_id=str(current_user.id))
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )
    recommendations = generate_improvement_recommendations(profile)
    return recommendations


@router.get("/{profile_id}", response_model=Profile)
async def read_profile(
    profile_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get profile by ID.
    """
    profile = get_profile(db, profile_id=profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )
    return profile 