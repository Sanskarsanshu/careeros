"""
CareerOS — Auth Service
"""
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserCreate, UserLogin, TokenResponse


class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def register_user(self, user_in: UserCreate) -> User:
        existing = await self.user_repo.get_by_email(user_in.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered."
            )
        
        user = User(
            email=user_in.email,
            password_hash=hash_password(user_in.password),
            full_name=user_in.full_name
        )
        return await self.user_repo.create(user)

    async def authenticate_user(self, user_in: UserLogin) -> TokenResponse:
        user = await self.user_repo.get_by_email(user_in.email)
        if not user or not user.password_hash:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not verify_password(user_in.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated."
            )
        
        return TokenResponse(
            access_token=create_access_token(subject=str(user.id)),
            refresh_token=create_refresh_token(subject=str(user.id)),
            token_type="bearer"
        )
