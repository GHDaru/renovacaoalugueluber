from abc import abstractmethod
from typing import Optional

from src.shared.domain.base_repository import BaseRepository
from src.domains.owner.domain.entities import Owner


class IOwnerRepository(BaseRepository[Owner]):
    @abstractmethod
    async def get_by_user_id(self, user_id) -> Optional[Owner]:
        ...
