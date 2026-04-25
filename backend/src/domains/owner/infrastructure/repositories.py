import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.owner.domain.entities import Owner
from src.domains.owner.domain.repositories import IOwnerRepository
from src.domains.owner.infrastructure.models import OwnerModel


def _to_entity(m: OwnerModel) -> Owner:
    return Owner(id=m.id, user_id=m.user_id, full_name=m.full_name, cpf=m.cpf,
                 phone=m.phone, address=m.address, is_verified=m.is_verified,
                 created_at=m.created_at, updated_at=m.updated_at)


def _to_model(e: Owner) -> OwnerModel:
    return OwnerModel(id=e.id, user_id=e.user_id, full_name=e.full_name, cpf=e.cpf,
                      phone=e.phone, address=e.address, is_verified=e.is_verified,
                      created_at=e.created_at, updated_at=e.updated_at)


class SQLAlchemyOwnerRepository(IOwnerRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, entity_id: uuid.UUID) -> Optional[Owner]:
        m = await self._session.get(OwnerModel, entity_id)
        return _to_entity(m) if m else None

    async def get_by_user_id(self, user_id: uuid.UUID) -> Optional[Owner]:
        result = await self._session.execute(select(OwnerModel).where(OwnerModel.user_id == user_id))
        m = result.scalar_one_or_none()
        return _to_entity(m) if m else None

    async def list_all(self) -> list[Owner]:
        result = await self._session.execute(select(OwnerModel))
        return [_to_entity(m) for m in result.scalars().all()]

    async def save(self, entity: Owner) -> Owner:
        entity.updated_at = datetime.now(timezone.utc)
        existing = await self._session.get(OwnerModel, entity.id)
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
        m = await self._session.get(OwnerModel, entity_id)
        if m:
            self._session.delete(m)
            await self._session.flush()
