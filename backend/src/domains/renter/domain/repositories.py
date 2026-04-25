from abc import abstractmethod
from typing import Optional

from src.shared.domain.base_repository import BaseRepository
from src.domains.renter.domain.entities import Renter


class IRenterRepository(BaseRepository[Renter]):
    @abstractmethod
    async def get_by_user_id(self, user_id) -> Optional[Renter]:
        ...
