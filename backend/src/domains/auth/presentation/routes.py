import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.database import get_db
from src.domains.auth.application.dtos import (
    LoginRequest,
    TokenResponse,
    UserCreate,
    UserPasswordUpdate,
    UserRead,
    UserUpdate,
)
from src.domains.auth.application.security import create_access_token, get_current_user, require_admin
from src.domains.auth.application.use_cases import (
    ChangeUserPassword,
    DeleteUser,
    ListUsers,
    LoginUser,
    RegisterUser,
    UpdateUser,
)
from src.domains.auth.infrastructure.repositories import SQLAlchemyUserRepository
from src.domains.auth.domain.entities import User

router = APIRouter(prefix="/auth", tags=["auth"])
users_router = APIRouter(prefix="/users", tags=["users"])


def _user_read(user: User) -> UserRead:
    return UserRead(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        is_active=user.is_active,
        created_at=user.created_at,
    )


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    repo = SQLAlchemyUserRepository(db)
    try:
        user = await RegisterUser(repo).execute(data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    return _user_read(user)


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
    return _user_read(current_user)


# ─── Admin user management ────────────────────────────────────────────────────

@users_router.get("", response_model=list[UserRead])
async def list_users(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    repo = SQLAlchemyUserRepository(db)
    users = await ListUsers(repo).execute()
    return [_user_read(u) for u in users]


@users_router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    repo = SQLAlchemyUserRepository(db)
    try:
        user = await RegisterUser(repo).execute(data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    return _user_read(user)


@users_router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: uuid.UUID,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    repo = SQLAlchemyUserRepository(db)
    try:
        user = await UpdateUser(repo).execute(user_id, data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return _user_read(user)


@users_router.put("/{user_id}/password", response_model=UserRead)
async def change_password(
    user_id: uuid.UUID,
    data: UserPasswordUpdate,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    repo = SQLAlchemyUserRepository(db)
    try:
        user = await ChangeUserPassword(repo).execute(user_id, data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return _user_read(user)


@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    repo = SQLAlchemyUserRepository(db)
    try:
        await DeleteUser(repo).execute(user_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
