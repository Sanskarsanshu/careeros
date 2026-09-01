"""
CareerOS — Auth API Routes
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin, UserResponse, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user via email and password."""
    auth_service = AuthService(db)
    return await auth_service.register_user(user_in)


@router.post("/login", response_model=TokenResponse)
async def login(
    user_in: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """Login to get access and refresh tokens."""
    auth_service = AuthService(db)
    return await auth_service.authenticate_user(user_in)


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user)
):
    """Get the currently authenticated user's profile."""
    return current_user
