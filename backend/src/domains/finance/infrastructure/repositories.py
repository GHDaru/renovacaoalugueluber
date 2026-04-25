import uuid
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.finance.domain.entities import VehicleCost, CostCategory
from src.domains.finance.domain.repositories import IVehicleCostRepository
from src.domains.finance.infrastructure.models import VehicleCostModel


def _to_entity(m: VehicleCostModel) -> VehicleCost:
    return VehicleCost(id=m.id, vehicle_id=m.vehicle_id, category=CostCategory(m.category),
                       description=m.description, amount=Decimal(str(m.amount)),
                       cost_date=m.cost_date, notes=m.notes,
                       created_at=m.created_at, updated_at=m.updated_at)


def _to_model(e: VehicleCost) -> VehicleCostModel:
    return VehicleCostModel(id=e.id, vehicle_id=e.vehicle_id, category=e.category.value,
                            description=e.description, amount=e.amount,
                            cost_date=e.cost_date, notes=e.notes,
                            created_at=e.created_at, updated_at=e.updated_at)


class SQLAlchemyVehicleCostRepository(IVehicleCostRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, entity_id: uuid.UUID) -> Optional[VehicleCost]:
        m = await self._session.get(VehicleCostModel, entity_id)
        return _to_entity(m) if m else None

    async def list_all(self) -> list[VehicleCost]:
        result = await self._session.execute(select(VehicleCostModel))
        return [_to_entity(m) for m in result.scalars().all()]

    async def list_by_vehicle(self, vehicle_id: uuid.UUID) -> list[VehicleCost]:
        result = await self._session.execute(
            select(VehicleCostModel).where(VehicleCostModel.vehicle_id == vehicle_id)
        )
        return [_to_entity(m) for m in result.scalars().all()]

    async def list_by_vehicle_and_period(
        self, vehicle_id: uuid.UUID, start_date: date, end_date: date
    ) -> list[VehicleCost]:
        result = await self._session.execute(
            select(VehicleCostModel).where(
                and_(
                    VehicleCostModel.vehicle_id == vehicle_id,
                    VehicleCostModel.cost_date >= start_date,
                    VehicleCostModel.cost_date <= end_date,
                )
            )
        )
        return [_to_entity(m) for m in result.scalars().all()]

    async def save(self, entity: VehicleCost) -> VehicleCost:
        entity.updated_at = datetime.now(timezone.utc)
        existing = await self._session.get(VehicleCostModel, entity.id)
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
        m = await self._session.get(VehicleCostModel, entity_id)
        if m:
            self._session.delete(m)
            await self._session.flush()
