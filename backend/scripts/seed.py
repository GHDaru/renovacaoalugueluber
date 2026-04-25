"""
Seed script – popula o banco com dados iniciais para desenvolvimento/homologação.

Execução (a partir do diretório backend/):
    python -m scripts.seed

O script cria:
  - 1 usuário ADMIN  (admin@renovacao.com / Admin@123)
  - 1 proprietário   (owner@renovacao.com / Owner@123)
  - 1 locatário      (renter@renovacao.com / Renter@123)
  - 1 veículo associado ao proprietário
"""

import asyncio
import uuid
from datetime import date, datetime, timezone

from sqlalchemy import select

from src.config import settings
from src.shared.infrastructure.database import AsyncSessionLocal, Base, engine
from src.domains.auth.infrastructure.models import UserModel
from src.domains.owner.infrastructure.models import OwnerModel
from src.domains.renter.infrastructure.models import RenterModel
from src.domains.vehicle.infrastructure.models import VehicleModel

# ──────────────────────────────────────────────────────────────
# Passlib é usado pelo domínio de auth; importamos diretamente.
# ──────────────────────────────────────────────────────────────
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _hash(password: str) -> str:
    return pwd_context.hash(password)


# ──────────────────────────────────────────────────────────────
# Dados seed
# ──────────────────────────────────────────────────────────────

ADMIN_ID = uuid.uuid4()
OWNER_USER_ID = uuid.uuid4()
RENTER_USER_ID = uuid.uuid4()
VEHICLE_ID = uuid.uuid4()

NOW = datetime.now(timezone.utc)

USERS = [
    UserModel(
        id=ADMIN_ID,
        email="admin@renovacao.com",
        hashed_password=_hash("Admin@123"),
        full_name="Administrador do Sistema",
        role="ADMIN",
        is_active=True,
        created_at=NOW,
        updated_at=NOW,
    ),
    UserModel(
        id=OWNER_USER_ID,
        email="owner@renovacao.com",
        hashed_password=_hash("Owner@123"),
        full_name="João Proprietário",
        role="OWNER",
        is_active=True,
        created_at=NOW,
        updated_at=NOW,
    ),
    UserModel(
        id=RENTER_USER_ID,
        email="renter@renovacao.com",
        hashed_password=_hash("Renter@123"),
        full_name="Maria Locatária",
        role="RENTER",
        is_active=True,
        created_at=NOW,
        updated_at=NOW,
    ),
]

OWNERS = [
    OwnerModel(
        id=uuid.uuid4(),
        user_id=OWNER_USER_ID,
        full_name="João Proprietário",
        cpf="12345678901",
        phone="11999990001",
        address="Av. Paulista, 1000, São Paulo – SP",
        is_verified=True,
        created_at=NOW,
        updated_at=NOW,
    )
]

RENTERS = [
    RenterModel(
        id=uuid.uuid4(),
        user_id=RENTER_USER_ID,
        full_name="Maria Locatária",
        cpf="98765432100",
        cnh="12345678",
        cnh_category="AB",
        cnh_expiry=date(2028, 12, 31),
        phone="11999990002",
        address="Rua das Flores, 50, São Paulo – SP",
        is_verified=True,
        created_at=NOW,
        updated_at=NOW,
    )
]

VEHICLES = [
    VehicleModel(
        id=VEHICLE_ID,
        owner_id=OWNERS[0].id,
        brand="Toyota",
        model="Corolla",
        year=2023,
        license_plate="ABC1D23",
        color="Prata",
        renavam="12345678901",
        chassis="9BW000000X0000001",
        status="AVAILABLE",
        daily_rate=180.00,
        description="Veículo em excelente estado, ar-condicionado, direção elétrica.",
        created_at=NOW,
        updated_at=NOW,
    )
]


# ──────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────

async def _exists(session, model, **filters) -> bool:
    conditions = [getattr(model, k) == v for k, v in filters.items()]
    result = await session.execute(select(model).where(*conditions))
    return result.scalars().first() is not None


async def seed() -> None:
    # Garante que todas as tabelas existam antes de inserir dados.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        # Users
        for user in USERS:
            if not await _exists(session, UserModel, email=user.email):
                session.add(user)
                print(f"  ✓ Usuário criado: {user.email} [{user.role}]")
            else:
                print(f"  – Usuário já existe: {user.email}")

        # Owners
        for owner in OWNERS:
            if not await _exists(session, OwnerModel, cpf=owner.cpf):
                session.add(owner)
                print(f"  ✓ Proprietário criado: {owner.full_name}")
            else:
                print(f"  – Proprietário já existe: CPF {owner.cpf}")

        # Renters
        for renter in RENTERS:
            if not await _exists(session, RenterModel, cpf=renter.cpf):
                session.add(renter)
                print(f"  ✓ Locatário criado: {renter.full_name}")
            else:
                print(f"  – Locatário já existe: CPF {renter.cpf}")

        # Vehicles
        for vehicle in VEHICLES:
            if not await _exists(session, VehicleModel, license_plate=vehicle.license_plate):
                session.add(vehicle)
                print(f"  ✓ Veículo criado: {vehicle.brand} {vehicle.model} ({vehicle.license_plate})")
            else:
                print(f"  – Veículo já existe: {vehicle.license_plate}")

        await session.commit()

    print("\nSeed concluído com sucesso.")


if __name__ == "__main__":
    print(f"\nConectando em: {settings.DATABASE_URL[:40]}...\n")
    asyncio.run(seed())
