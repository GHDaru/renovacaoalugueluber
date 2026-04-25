import uuid
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.rental.domain.entities import Rental, RentalStatus
from src.domains.rental.domain.repositories import IRentalRepository
from src.domains.rental.infrastructure.models import RentalModel


def _to_entity(m: RentalModel) -> Rental:
    return Rental(id=m.id, vehicle_id=m.vehicle_id, renter_id=m.renter_id,
                  start_date=m.start_date, end_date=m.end_date,
                  daily_rate=Decimal(str(m.daily_rate)),
                  total_amount=Decimal(str(m.total_amount)),
                  status=RentalStatus(m.status), notes=m.notes,
                  created_at=m.created_at, updated_at=m.updated_at)


def _to_model(e: Rental) -> RentalModel:
    return RentalModel(id=e.id, vehicle_id=e.vehicle_id, renter_id=e.renter_id,
                       start_date=e.start_date, end_date=e.end_date,
                       daily_rate=e.daily_rate, total_amount=e.total_amount,
                       status=e.status.value, notes=e.notes,
                       created_at=e.created_at, updated_at=e.updated_at)


class SQLAlchemyRentalRepository(IRentalRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, entity_id: uuid.UUID) -> Optional[Rental]:
        m = await self._session.get(RentalModel, entity_id)
        return _to_entity(m) if m else None

    async def list_all(self) -> list[Rental]:
        result = await self._session.execute(select(RentalModel))
        return [_to_entity(m) for m in result.scalars().all()]

    async def list_by_vehicle(self, vehicle_id: uuid.UUID) -> list[Rental]:
        result = await self._session.execute(
            select(RentalModel).where(RentalModel.vehicle_id == vehicle_id)
        )
        return [_to_entity(m) for m in result.scalars().all()]

    async def list_by_renter(self, renter_id: uuid.UUID) -> list[Rental]:
        result = await self._session.execute(
            select(RentalModel).where(RentalModel.renter_id == renter_id)
        )
        return [_to_entity(m) for m in result.scalars().all()]

    async def list_active(self) -> list[Rental]:
        result = await self._session.execute(
            select(RentalModel).where(RentalModel.status == RentalStatus.ACTIVE.value)
        )
        return [_to_entity(m) for m in result.scalars().all()]

    async def list_completed_by_vehicle_and_period(
        self, vehicle_id: uuid.UUID, start_date: date, end_date: date
    ) -> list[Rental]:
        result = await self._session.execute(
            select(RentalModel).where(
                and_(
                    RentalModel.vehicle_id == vehicle_id,
                    RentalModel.status == RentalStatus.COMPLETED.value,
                    RentalModel.start_date >= start_date,
                    RentalModel.end_date <= end_date,
                )
            )
        )
        return [_to_entity(m) for m in result.scalars().all()]

    async def save(self, entity: Rental) -> Rental:
        entity.updated_at = datetime.now(timezone.utc)
        existing = await self._session.get(RentalModel, entity.id)
        if existing:
            for k, v in vars(_to_model(entity)).items():
                if not k.startswith("_"):
                    setattr(existing, k, v)
            m = existing
        else:
            m = _to_model(entity)
            self._session.add(m)
        await self._session.flush()
        return _to_entity(m)

    async def delete(self, entity_id: uuid.UUID) -> None:
        m = await self._session.get(RentalModel, entity_id)
        if m:
            await self._session.delete(m)
            await self._session.flush()
