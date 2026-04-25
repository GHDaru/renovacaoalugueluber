from abc import abstractmethod

from src.shared.domain.base_repository import BaseRepository
from src.domains.rental.domain.entities import Rental


class IRentalRepository(BaseRepository[Rental]):
    @abstractmethod
    async def list_by_vehicle(self, vehicle_id) -> list[Rental]:
        ...

    @abstractmethod
    async def list_by_renter(self, renter_id) -> list[Rental]:
        ...

    @abstractmethod
    async def list_active(self) -> list[Rental]:
        ...

    @abstractmethod
    async def list_completed_by_vehicle_and_period(self, vehicle_id, start_date, end_date) -> list[Rental]:
        ...
