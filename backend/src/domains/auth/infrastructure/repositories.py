import uuid
from datetime import timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.auth.domain.entities import User, UserRole
from src.domains.auth.domain.repositories import IUserRepository
from src.domains.auth.infrastructure.models import UserModel


def _to_entity(m: UserModel) -> User:
    return User(
        id=m.id,
        email=m.email,
        hashed_password=m.hashed_password,
        full_name=m.full_name,
        role=UserRole(m.role),
        is_active=m.is_active,
        created_at=m.created_at,
        updated_at=m.updated_at,
    )


def _to_model(e: User) -> UserModel:
    return UserModel(
        id=e.id,
        email=e.email,
        hashed_password=e.hashed_password,
        full_name=e.full_name,
        role=e.role.value,
        is_active=e.is_active,
        created_at=e.created_at,
        updated_at=e.updated_at,
    )


class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, entity_id: uuid.UUID) -> Optional[User]:
        result = await self._session.get(UserModel, entity_id)
        return _to_entity(result) if result else None

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self._session.execute(select(UserModel).where(UserModel.email == email))
        m = result.scalar_one_or_none()
        return _to_entity(m) if m else None

    async def list_all(self) -> list[User]:
        result = await self._session.execute(select(UserModel))
        return [_to_entity(m) for m in result.scalars().all()]

    async def save(self, entity: User) -> User:
        from datetime import datetime
        entity.updated_at = datetime.now(timezone.utc)
        existing = await self._session.get(UserModel, entity.id)
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
        m = await self._session.get(UserModel, entity_id)
        if m:
            await self._session.delete(m)
            await self._session.flush()
