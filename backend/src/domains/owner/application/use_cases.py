import uuid
from datetime import datetime, timezone

from src.domains.owner.domain.entities import Owner
from src.domains.owner.domain.repositories import IOwnerRepository
from src.domains.owner.application.dtos import OwnerCreate, OwnerUpdate


class RegisterOwner:
    def __init__(self, repo: IOwnerRepository) -> None:
        self._repo = repo

    async def execute(self, user_id: uuid.UUID, data: OwnerCreate) -> Owner:
        owner = Owner(user_id=user_id, full_name=data.full_name, cpf=data.cpf,
                      phone=data.phone, address=data.address)
        return await self._repo.save(owner)


class GetOwner:
    def __init__(self, repo: IOwnerRepository) -> None:
        self._repo = repo

    async def execute(self, owner_id: uuid.UUID) -> Owner:
        owner = await self._repo.get_by_id(owner_id)
        if not owner:
            raise ValueError("Proprietário não encontrado.")
        return owner


class UpdateOwner:
    def __init__(self, repo: IOwnerRepository) -> None:
        self._repo = repo

    async def execute(self, owner_id: uuid.UUID, data: OwnerUpdate) -> Owner:
        owner = await self._repo.get_by_id(owner_id)
        if not owner:
            raise ValueError("Proprietário não encontrado.")
        if data.full_name is not None:
            owner.full_name = data.full_name
        if data.phone is not None:
            owner.phone = data.phone
        if data.address is not None:
            owner.address = data.address
        owner.updated_at = datetime.now(timezone.utc)
        return await self._repo.save(owner)


class VerifyOwner:
    def __init__(self, repo: IOwnerRepository) -> None:
        self._repo = repo

    async def execute(self, owner_id: uuid.UUID) -> Owner:
        owner = await self._repo.get_by_id(owner_id)
        if not owner:
            raise ValueError("Proprietário não encontrado.")
        owner.is_verified = True
        owner.updated_at = datetime.now(timezone.utc)
        return await self._repo.save(owner)
