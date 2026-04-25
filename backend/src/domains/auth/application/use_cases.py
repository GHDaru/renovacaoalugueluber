from src.domains.auth.domain.entities import User
from src.domains.auth.domain.repositories import IUserRepository
from src.domains.auth.application.dtos import UserCreate, LoginRequest
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
