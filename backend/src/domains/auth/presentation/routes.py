from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.database import get_db
from src.domains.auth.application.dtos import LoginRequest, TokenResponse, UserCreate, UserRead
from src.domains.auth.application.security import create_access_token, get_current_user
from src.domains.auth.application.use_cases import LoginUser, RegisterUser
from src.domains.auth.infrastructure.repositories import SQLAlchemyUserRepository
from src.domains.auth.domain.entities import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    repo = SQLAlchemyUserRepository(db)
    try:
        user = await RegisterUser(repo).execute(data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    return UserRead(
        id=str(user.id), email=user.email, full_name=user.full_name,
        role=user.role, is_active=user.is_active, created_at=user.created_at,
    )


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    repo = SQLAlchemyUserRepository(db)
    try:
        user = await LoginUser(repo).execute(data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))
    token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserRead)
async def me(current_user: User = Depends(get_current_user)):
    return UserRead(
        id=str(current_user.id), email=current_user.email,
        full_name=current_user.full_name, role=current_user.role,
        is_active=current_user.is_active, created_at=current_user.created_at,
    )
