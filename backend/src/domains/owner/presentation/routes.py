import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.database import get_db
from src.domains.auth.application.security import get_current_user
from src.domains.auth.domain.entities import User, UserRole
from src.domains.owner.application.dtos import OwnerCreate, OwnerRead, OwnerUpdate
from src.domains.owner.application.use_cases import GetOwner, RegisterOwner, UpdateOwner, VerifyOwner
from src.domains.owner.infrastructure.repositories import SQLAlchemyOwnerRepository

router = APIRouter(prefix="/owners", tags=["owners"])


def _read(o) -> OwnerRead:
    return OwnerRead(id=str(o.id), user_id=str(o.user_id), full_name=o.full_name,
                     cpf=o.cpf, phone=o.phone, address=o.address,
                     is_verified=o.is_verified, created_at=o.created_at, updated_at=o.updated_at)


@router.post("/", response_model=OwnerRead, status_code=status.HTTP_201_CREATED)
async def register_owner(
    data: OwnerCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = SQLAlchemyOwnerRepository(db)
    owner = await RegisterOwner(repo).execute(current_user.id, data)
    return _read(owner)


@router.get("/{owner_id}", response_model=OwnerRead)
async def get_owner(
    owner_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = SQLAlchemyOwnerRepository(db)
    try:
        return _read(await GetOwner(repo).execute(owner_id))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.put("/{owner_id}", response_model=OwnerRead)
async def update_owner(
    owner_id: uuid.UUID,
    data: OwnerUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = SQLAlchemyOwnerRepository(db)
    try:
        return _read(await UpdateOwner(repo).execute(owner_id, data))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post("/{owner_id}/verify", response_model=OwnerRead)
async def verify_owner(
    owner_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso restrito a administradores.")
    repo = SQLAlchemyOwnerRepository(db)
    try:
        return _read(await VerifyOwner(repo).execute(owner_id))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
