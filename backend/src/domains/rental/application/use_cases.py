import uuid
from datetime import datetime, timezone
from decimal import Decimal

from src.domains.rental.domain.entities import Rental, RentalStatus
from src.domains.rental.domain.repositories import IRentalRepository
from src.domains.rental.application.dtos import RentalCreate


class CreateRental:
    def __init__(self, repo: IRentalRepository) -> None:
        self._repo = repo

    async def execute(self, renter_id: uuid.UUID, data: RentalCreate) -> Rental:
        days = (data.end_date - data.start_date).days
        if days <= 0:
            raise ValueError("Data de fim deve ser posterior à data de início.")
        total = data.daily_rate * Decimal(days)
        rental = Rental(
            vehicle_id=uuid.UUID(data.vehicle_id),
            renter_id=renter_id,
            start_date=data.start_date,
            end_date=data.end_date,
            daily_rate=data.daily_rate,
            total_amount=total,
        )
        return await self._repo.save(rental)


class ActivateRental:
    def __init__(self, repo: IRentalRepository) -> None:
        self._repo = repo

    async def execute(self, rental_id: uuid.UUID) -> Rental:
        r = await self._repo.get_by_id(rental_id)
        if not r:
            raise ValueError("Locação não encontrada.")
        if r.status != RentalStatus.PENDING:
            raise ValueError("Apenas locações pendentes podem ser ativadas.")
        r.status = RentalStatus.ACTIVE
        r.updated_at = datetime.now(timezone.utc)
        return await self._repo.save(r)


class CompleteRental:
    def __init__(self, repo: IRentalRepository) -> None:
        self._repo = repo

    async def execute(self, rental_id: uuid.UUID) -> Rental:
        r = await self._repo.get_by_id(rental_id)
        if not r:
            raise ValueError("Locação não encontrada.")
        if r.status != RentalStatus.ACTIVE:
            raise ValueError("Apenas locações ativas podem ser concluídas.")
        r.status = RentalStatus.COMPLETED
        r.updated_at = datetime.now(timezone.utc)
        return await self._repo.save(r)


class CancelRental:
    def __init__(self, repo: IRentalRepository) -> None:
        self._repo = repo

    async def execute(self, rental_id: uuid.UUID) -> Rental:
        r = await self._repo.get_by_id(rental_id)
        if not r:
            raise ValueError("Locação não encontrada.")
        if r.status in (RentalStatus.COMPLETED, RentalStatus.CANCELLED):
            raise ValueError("Locação já finalizada.")
        r.status = RentalStatus.CANCELLED
        r.updated_at = datetime.now(timezone.utc)
        return await self._repo.save(r)


class GetRentalsByVehicle:
    def __init__(self, repo: IRentalRepository) -> None:
        self._repo = repo

    async def execute(self, vehicle_id: uuid.UUID) -> list[Rental]:
        return await self._repo.list_by_vehicle(vehicle_id)
