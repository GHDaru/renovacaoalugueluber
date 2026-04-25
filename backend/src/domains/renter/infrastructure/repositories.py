import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.renter.domain.entities import Renter
from src.domains.renter.domain.repositories import IRenterRepository
from src.domains.renter.infrastructure.models import RenterModel


def _to_entity(m: RenterModel) -> Renter:
    return Renter(id=m.id, user_id=m.user_id, full_name=m.full_name, cpf=m.cpf,
                  cnh=m.cnh, cnh_category=m.cnh_category, cnh_expiry=m.cnh_expiry,
                  phone=m.phone, address=m.address, is_verified=m.is_verified,
                  created_at=m.created_at, updated_at=m.updated_at)


def _to_model(e: Renter) -> RenterModel:
    return RenterModel(id=e.id, user_id=e.user_id, full_name=e.full_name, cpf=e.cpf,
                       cnh=e.cnh, cnh_category=e.cnh_category, cnh_expiry=e.cnh_expiry,
                       phone=e.phone, address=e.address, is_verified=e.is_verified,
                       created_at=e.created_at, updated_at=e.updated_at)


class SQLAlchemyRenterRepository(IRenterRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, entity_id: uuid.UUID) -> Optional[Renter]:
        m = await self._session.get(RenterModel, entity_id)
        return _to_entity(m) if m else None

    async def get_by_user_id(self, user_id: uuid.UUID) -> Optional[Renter]:
        result = await self._session.execute(select(RenterModel).where(RenterModel.user_id == user_id))
        m = result.scalar_one_or_none()
        return _to_entity(m) if m else None

    async def list_all(self) -> list[Renter]:
        result = await self._session.execute(select(RenterModel))
        return [_to_entity(m) for m in result.scalars().all()]

    async def save(self, entity: Renter) -> Renter:
        entity.updated_at = datetime.now(timezone.utc)
        existing = await self._session.get(RenterModel, entity.id)
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
        m = await self._session.get(RenterModel, entity_id)
        if m:
            self._session.delete(m)
            await self._session.flush()
