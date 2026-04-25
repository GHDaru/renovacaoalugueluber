from abc import abstractmethod
from typing import Optional

from src.shared.domain.base_repository import BaseRepository
from src.domains.auth.domain.entities import User


class IUserRepository(BaseRepository[User]):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        ...
