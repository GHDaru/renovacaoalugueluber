from abc import abstractmethod
from typing import Optional

from src.shared.domain.base_repository import BaseRepository
from src.domains.vehicle.domain.entities import Vehicle, VehicleDocument


class IVehicleRepository(BaseRepository[Vehicle]):
    @abstractmethod
    async def list_by_owner(self, owner_id) -> list[Vehicle]:
        ...

    @abstractmethod
    async def list_approved(self) -> list[Vehicle]:
        ...


class IVehicleDocumentRepository(BaseRepository[VehicleDocument]):
    @abstractmethod
    async def list_by_vehicle(self, vehicle_id) -> list[VehicleDocument]:
        ...
