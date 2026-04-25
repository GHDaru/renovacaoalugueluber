import uuid
from datetime import datetime, timezone

from src.domains.renter.domain.entities import Renter
from src.domains.renter.domain.repositories import IRenterRepository
from src.domains.renter.application.dtos import RenterCreate, RenterUpdate


class RegisterRenter:
    def __init__(self, repo: IRenterRepository) -> None:
        self._repo = repo

    async def execute(self, user_id: uuid.UUID, data: RenterCreate) -> Renter:
        renter = Renter(user_id=user_id, full_name=data.full_name, cpf=data.cpf,
                        cnh=data.cnh, cnh_category=data.cnh_category,
                        cnh_expiry=data.cnh_expiry, phone=data.phone, address=data.address)
        return await self._repo.save(renter)


class GetRenter:
    def __init__(self, repo: IRenterRepository) -> None:
        self._repo = repo

    async def execute(self, renter_id: uuid.UUID) -> Renter:
        r = await self._repo.get_by_id(renter_id)
        if not r:
            raise ValueError("Locatário não encontrado.")
        return r


class UpdateRenter:
    def __init__(self, repo: IRenterRepository) -> None:
        self._repo = repo

    async def execute(self, renter_id: uuid.UUID, data: RenterUpdate) -> Renter:
        r = await self._repo.get_by_id(renter_id)
        if not r:
            raise ValueError("Locatário não encontrado.")
        if data.full_name is not None:
            r.full_name = data.full_name
        if data.phone is not None:
            r.phone = data.phone
        if data.address is not None:
            r.address = data.address
        if data.cnh_expiry is not None:
            r.cnh_expiry = data.cnh_expiry
        r.updated_at = datetime.now(timezone.utc)
        return await self._repo.save(r)


class VerifyRenter:
    def __init__(self, repo: IRenterRepository) -> None:
        self._repo = repo

    async def execute(self, renter_id: uuid.UUID) -> Renter:
        r = await self._repo.get_by_id(renter_id)
        if not r:
            raise ValueError("Locatário não encontrado.")
        r.is_verified = True
        r.updated_at = datetime.now(timezone.utc)
        return await self._repo.save(r)
