import uuid
from datetime import datetime, timezone

from src.domains.vehicle.domain.entities import Vehicle, VehicleDocument, VehicleStatus
from src.domains.vehicle.domain.repositories import IVehicleRepository, IVehicleDocumentRepository
from src.domains.vehicle.application.dtos import VehicleCreate, VehicleUpdate, VehicleDocumentCreate


class RegisterVehicle:
    def __init__(self, repo: IVehicleRepository) -> None:
        self._repo = repo

    async def execute(self, owner_id: uuid.UUID, data: VehicleCreate) -> Vehicle:
        vehicle = Vehicle(owner_id=owner_id, brand=data.brand, model=data.model,
                          year=data.year, license_plate=data.license_plate, color=data.color,
                          renavam=data.renavam, chassis=data.chassis,
                          daily_rate=data.daily_rate, description=data.description)
        return await self._repo.save(vehicle)


class GetVehicle:
    def __init__(self, repo: IVehicleRepository) -> None:
        self._repo = repo

    async def execute(self, vehicle_id: uuid.UUID) -> Vehicle:
        v = await self._repo.get_by_id(vehicle_id)
        if not v:
            raise ValueError("Veículo não encontrado.")
        return v


class UpdateVehicle:
    def __init__(self, repo: IVehicleRepository) -> None:
        self._repo = repo

    async def execute(self, vehicle_id: uuid.UUID, data: VehicleUpdate) -> Vehicle:
        v = await self._repo.get_by_id(vehicle_id)
        if not v:
            raise ValueError("Veículo não encontrado.")
        if data.brand is not None:
            v.brand = data.brand
        if data.model is not None:
            v.model = data.model
        if data.year is not None:
            v.year = data.year
        if data.color is not None:
            v.color = data.color
        if data.daily_rate is not None:
            v.daily_rate = data.daily_rate
        if data.description is not None:
            v.description = data.description
        v.updated_at = datetime.now(timezone.utc)
        return await self._repo.save(v)


class ApproveVehicle:
    def __init__(self, repo: IVehicleRepository) -> None:
        self._repo = repo

    async def execute(self, vehicle_id: uuid.UUID) -> Vehicle:
        v = await self._repo.get_by_id(vehicle_id)
        if not v:
            raise ValueError("Veículo não encontrado.")
        v.status = VehicleStatus.APPROVED
        v.updated_at = datetime.now(timezone.utc)
        return await self._repo.save(v)


class RejectVehicle:
    def __init__(self, repo: IVehicleRepository) -> None:
        self._repo = repo

    async def execute(self, vehicle_id: uuid.UUID) -> Vehicle:
        v = await self._repo.get_by_id(vehicle_id)
        if not v:
            raise ValueError("Veículo não encontrado.")
        v.status = VehicleStatus.REJECTED
        v.updated_at = datetime.now(timezone.utc)
        return await self._repo.save(v)


class SuspendVehicle:
    def __init__(self, repo: IVehicleRepository) -> None:
        self._repo = repo

    async def execute(self, vehicle_id: uuid.UUID) -> Vehicle:
        v = await self._repo.get_by_id(vehicle_id)
        if not v:
            raise ValueError("Veículo não encontrado.")
        v.status = VehicleStatus.SUSPENDED
        v.updated_at = datetime.now(timezone.utc)
        return await self._repo.save(v)


class ListApprovedVehicles:
    def __init__(self, repo: IVehicleRepository) -> None:
        self._repo = repo

    async def execute(self) -> list[Vehicle]:
        return await self._repo.list_approved()


class UploadDocument:
    def __init__(self, repo: IVehicleDocumentRepository) -> None:
        self._repo = repo

    async def execute(self, vehicle_id: uuid.UUID, data: VehicleDocumentCreate) -> VehicleDocument:
        doc = VehicleDocument(vehicle_id=vehicle_id, document_type=data.document_type,
                              file_url=data.file_url)
        return await self._repo.save(doc)
