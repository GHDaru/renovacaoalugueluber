import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.vehicle.domain.entities import Vehicle, VehicleDocument, VehicleStatus
from src.domains.vehicle.domain.repositories import IVehicleRepository, IVehicleDocumentRepository
from src.domains.vehicle.infrastructure.models import VehicleModel, VehicleDocumentModel


# ─── Vehicle ─────────────────────────────────────────────────────────────────

def _v_to_entity(m: VehicleModel) -> Vehicle:
    return Vehicle(id=m.id, owner_id=m.owner_id, brand=m.brand, model=m.model,
                   year=m.year, license_plate=m.license_plate, color=m.color,
                   renavam=m.renavam, chassis=m.chassis, status=VehicleStatus(m.status),
                   daily_rate=Decimal(str(m.daily_rate)), description=m.description,
                   created_at=m.created_at, updated_at=m.updated_at)


def _v_to_model(e: Vehicle) -> VehicleModel:
    return VehicleModel(id=e.id, owner_id=e.owner_id, brand=e.brand, model=e.model,
                        year=e.year, license_plate=e.license_plate, color=e.color,
                        renavam=e.renavam, chassis=e.chassis, status=e.status.value,
                        daily_rate=e.daily_rate, description=e.description,
                        created_at=e.created_at, updated_at=e.updated_at)


class SQLAlchemyVehicleRepository(IVehicleRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, entity_id: uuid.UUID) -> Optional[Vehicle]:
        m = await self._session.get(VehicleModel, entity_id)
        return _v_to_entity(m) if m else None

    async def list_all(self) -> list[Vehicle]:
        result = await self._session.execute(select(VehicleModel))
        return [_v_to_entity(m) for m in result.scalars().all()]

    async def list_by_owner(self, owner_id: uuid.UUID) -> list[Vehicle]:
        result = await self._session.execute(select(VehicleModel).where(VehicleModel.owner_id == owner_id))
        return [_v_to_entity(m) for m in result.scalars().all()]

    async def list_approved(self) -> list[Vehicle]:
        result = await self._session.execute(
            select(VehicleModel).where(VehicleModel.status == VehicleStatus.APPROVED.value)
        )
        return [_v_to_entity(m) for m in result.scalars().all()]

    async def save(self, entity: Vehicle) -> Vehicle:
        entity.updated_at = datetime.now(timezone.utc)
        existing = await self._session.get(VehicleModel, entity.id)
        if existing:
            for k, v in vars(_v_to_model(entity)).items():
                if not k.startswith("_"):
                    setattr(existing, k, v)
            m = existing
        else:
            m = _v_to_model(entity)
            self._session.add(m)
        await self._session.flush()
        return _v_to_entity(m)

    async def delete(self, entity_id: uuid.UUID) -> None:
        m = await self._session.get(VehicleModel, entity_id)
        if m:
            self._session.delete(m)
            await self._session.flush()


# ─── VehicleDocument ─────────────────────────────────────────────────────────

def _d_to_entity(m: VehicleDocumentModel) -> VehicleDocument:
    return VehicleDocument(id=m.id, vehicle_id=m.vehicle_id, document_type=m.document_type,
                           file_url=m.file_url, is_approved=m.is_approved,
                           created_at=m.created_at, updated_at=m.updated_at)


def _d_to_model(e: VehicleDocument) -> VehicleDocumentModel:
    return VehicleDocumentModel(id=e.id, vehicle_id=e.vehicle_id, document_type=e.document_type,
                                file_url=e.file_url, is_approved=e.is_approved,
                                created_at=e.created_at, updated_at=e.updated_at)


class SQLAlchemyVehicleDocumentRepository(IVehicleDocumentRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, entity_id: uuid.UUID) -> Optional[VehicleDocument]:
        m = await self._session.get(VehicleDocumentModel, entity_id)
        return _d_to_entity(m) if m else None

    async def list_all(self) -> list[VehicleDocument]:
        result = await self._session.execute(select(VehicleDocumentModel))
        return [_d_to_entity(m) for m in result.scalars().all()]

    async def list_by_vehicle(self, vehicle_id: uuid.UUID) -> list[VehicleDocument]:
        result = await self._session.execute(
            select(VehicleDocumentModel).where(VehicleDocumentModel.vehicle_id == vehicle_id)
        )
        return [_d_to_entity(m) for m in result.scalars().all()]

    async def save(self, entity: VehicleDocument) -> VehicleDocument:
        entity.updated_at = datetime.now(timezone.utc)
        existing = await self._session.get(VehicleDocumentModel, entity.id)
        if existing:
            for k, v in vars(_d_to_model(entity)).items():
                if not k.startswith("_"):
                    setattr(existing, k, v)
            m = existing
        else:
            m = _d_to_model(entity)
            self._session.add(m)
        await self._session.flush()
        return _d_to_entity(m)

    async def delete(self, entity_id: uuid.UUID) -> None:
        m = await self._session.get(VehicleDocumentModel, entity_id)
        if m:
            self._session.delete(m)
            await self._session.flush()
