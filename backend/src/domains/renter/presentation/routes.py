import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.database import get_db
from src.domains.auth.application.security import get_current_user
from src.domains.auth.domain.entities import User, UserRole
from src.domains.renter.application.dtos import RenterCreate, RenterRead, RenterUpdate
from src.domains.renter.application.use_cases import GetRenter, RegisterRenter, UpdateRenter, VerifyRenter
from src.domains.renter.infrastructure.repositories import SQLAlchemyRenterRepository

router = APIRouter(prefix="/renters", tags=["renters"])


def _read(r) -> RenterRead:
    return RenterRead(id=str(r.id), user_id=str(r.user_id), full_name=r.full_name,
                      cpf=r.cpf, cnh=r.cnh, cnh_category=r.cnh_category,
                      cnh_expiry=r.cnh_expiry, phone=r.phone, address=r.address,
                      is_verified=r.is_verified, created_at=r.created_at, updated_at=r.updated_at)


@router.post("/", response_model=RenterRead, status_code=status.HTTP_201_CREATED)
async def register_renter(
    data: RenterCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = SQLAlchemyRenterRepository(db)
    return _read(await RegisterRenter(repo).execute(current_user.id, data))


@router.get("/{renter_id}", response_model=RenterRead)
async def get_renter(
    renter_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = SQLAlchemyRenterRepository(db)
    try:
        return _read(await GetRenter(repo).execute(renter_id))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.put("/{renter_id}", response_model=RenterRead)
async def update_renter(
    renter_id: uuid.UUID,
    data: RenterUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = SQLAlchemyRenterRepository(db)
    try:
        return _read(await UpdateRenter(repo).execute(renter_id, data))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post("/{renter_id}/verify", response_model=RenterRead)
async def verify_renter(
    renter_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso restrito a administradores.")
    repo = SQLAlchemyRenterRepository(db)
    try:
        return _read(await VerifyRenter(repo).execute(renter_id))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
