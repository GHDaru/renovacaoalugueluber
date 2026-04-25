import uuid
from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

from src.shared.domain.base_entity import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    async def get_by_id(self, entity_id: uuid.UUID) -> Optional[T]:
        ...

    @abstractmethod
    async def list_all(self) -> list[T]:
        ...

    @abstractmethod
    async def save(self, entity: T) -> T:
        ...

    @abstractmethod
    async def delete(self, entity_id: uuid.UUID) -> None:
        ...
