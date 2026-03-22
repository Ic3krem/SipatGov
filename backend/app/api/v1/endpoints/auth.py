from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

router = APIRouter()


@router.post("/register")
async def register(db: AsyncSession = Depends(get_db)):
    """Register a new user with email/phone + password."""
    return {"message": "registration endpoint - TODO"}


@router.post("/login")
async def login(db: AsyncSession = Depends(get_db)):
    """Login and receive JWT access + refresh tokens."""
    return {"message": "login endpoint - TODO"}


@router.post("/refresh")
async def refresh_token():
    """Refresh an expired access token."""
    return {"message": "refresh endpoint - TODO"}


@router.get("/me")
async def get_current_user(db: AsyncSession = Depends(get_db)):
    """Get the current authenticated user's profile."""
    return {"message": "me endpoint - TODO"}


@router.patch("/me")
async def update_profile(db: AsyncSession = Depends(get_db)):
    """Update user profile (display_name, home_lgu_id, avatar)."""
    return {"message": "update profile endpoint - TODO"}


@router.post("/me/onboarding")
async def complete_onboarding(db: AsyncSession = Depends(get_db)):
    """Mark onboarding as completed, save region/LGU preference."""
    return {"message": "onboarding endpoint - TODO"}
