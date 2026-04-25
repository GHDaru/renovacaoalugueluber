from abc import abstractmethod
from datetime import date

from src.shared.domain.base_repository import BaseRepository
from src.domains.finance.domain.entities import VehicleCost


class IVehicleCostRepository(BaseRepository[VehicleCost]):
    @abstractmethod
    async def list_by_vehicle(self, vehicle_id) -> list[VehicleCost]:
        ...

    @abstractmethod
    async def list_by_vehicle_and_period(self, vehicle_id, start_date: date, end_date: date) -> list[VehicleCost]:
        ...
