import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.database import get_db
from src.domains.auth.application.security import get_current_user
from src.domains.auth.domain.entities import User
from src.domains.rental.application.dtos import RentalCreate, RentalRead
from src.domains.rental.application.use_cases import (
    CreateRental, ActivateRental, CompleteRental, CancelRental, GetRentalsByVehicle,
)
from src.domains.rental.infrastructure.repositories import SQLAlchemyRentalRepository

router = APIRouter(prefix="/rentals", tags=["rentals"])


def _read(r) -> RentalRead:
    return RentalRead(
        id=str(r.id), vehicle_id=str(r.vehicle_id), renter_id=str(r.renter_id),
        start_date=r.start_date, end_date=r.end_date, daily_rate=r.daily_rate,
        total_amount=r.total_amount, status=r.status, notes=r.notes,
        created_at=r.created_at, updated_at=r.updated_at,
    )


@router.post("/", response_model=RentalRead, status_code=status.HTTP_201_CREATED)
async def create_rental(
    data: RentalCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = SQLAlchemyRentalRepository(db)
    try:
        return _read(await CreateRental(repo).execute(current_user.id, data))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/", response_model=list[RentalRead])
async def list_rentals(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = SQLAlchemyRentalRepository(db)
    rentals = await repo.list_by_renter(current_user.id)
    return [_read(r) for r in rentals]


@router.get("/{rental_id}", response_model=RentalRead)
async def get_rental(
    rental_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = SQLAlchemyRentalRepository(db)
    r = await repo.get_by_id(rental_id)
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Locação não encontrada.")
    return _read(r)


@router.put("/{rental_id}/activate", response_model=RentalRead)
async def activate_rental(
    rental_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = SQLAlchemyRentalRepository(db)
    try:
        return _read(await ActivateRental(repo).execute(rental_id))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.put("/{rental_id}/complete", response_model=RentalRead)
async def complete_rental(
    rental_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = SQLAlchemyRentalRepository(db)
    try:
        return _read(await CompleteRental(repo).execute(rental_id))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.put("/{rental_id}/cancel", response_model=RentalRead)
async def cancel_rental(
    rental_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = SQLAlchemyRentalRepository(db)
    try:
        return _read(await CancelRental(repo).execute(rental_id))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
