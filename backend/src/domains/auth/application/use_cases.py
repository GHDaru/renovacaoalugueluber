import uuid

from src.domains.auth.domain.entities import User
from src.domains.auth.domain.repositories import IUserRepository
from src.domains.auth.application.dtos import UserCreate, UserUpdate, UserPasswordUpdate, LoginRequest
from src.domains.auth.application.security import get_password_hash, verify_password


class RegisterUser:
    def __init__(self, repo: IUserRepository) -> None:
        self._repo = repo

    async def execute(self, data: UserCreate) -> User:
        existing = await self._repo.get_by_email(data.email)
        if existing:
            raise ValueError("E-mail já cadastrado.")
        user = User(
            email=data.email,
            hashed_password=get_password_hash(data.password),
            full_name=data.full_name,
            role=data.role,
        )
        return await self._repo.save(user)


class LoginUser:
    def __init__(self, repo: IUserRepository) -> None:
        self._repo = repo

    async def execute(self, data: LoginRequest) -> User:
        user = await self._repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.hashed_password):
            raise ValueError("Credenciais inválidas.")
        if not user.is_active:
            raise ValueError("Conta desativada.")
        return user


class ListUsers:
    def __init__(self, repo: IUserRepository) -> None:
        self._repo = repo

    async def execute(self) -> list[User]:
        return await self._repo.list_all()


class UpdateUser:
    def __init__(self, repo: IUserRepository) -> None:
        self._repo = repo

    async def execute(self, user_id: uuid.UUID, data: UserUpdate) -> User:
        user = await self._repo.get_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado.")
        if data.full_name is not None:
            user.full_name = data.full_name
        if data.role is not None:
            user.role = data.role
        if data.is_active is not None:
            user.is_active = data.is_active
        return await self._repo.save(user)


class ChangeUserPassword:
    def __init__(self, repo: IUserRepository) -> None:
        self._repo = repo

    async def execute(self, user_id: uuid.UUID, data: UserPasswordUpdate) -> User:
        user = await self._repo.get_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado.")
        user.hashed_password = get_password_hash(data.new_password)
        return await self._repo.save(user)


class DeleteUser:
    def __init__(self, repo: IUserRepository) -> None:
        self._repo = repo

    async def execute(self, user_id: uuid.UUID) -> None:
        user = await self._repo.get_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado.")
        await self._repo.delete(user_id)
