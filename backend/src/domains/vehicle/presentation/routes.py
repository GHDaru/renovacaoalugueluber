import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.database import get_db
from src.domains.auth.application.security import get_current_user
from src.domains.auth.domain.entities import User, UserRole
from src.domains.vehicle.application.dtos import (
    VehicleCreate, VehicleRead, VehicleUpdate,
    VehicleDocumentCreate, VehicleDocumentRead,
)
from src.domains.vehicle.application.use_cases import (
    RegisterVehicle, GetVehicle, UpdateVehicle, ApproveVehicle, RejectVehicle,
    SuspendVehicle, ListApprovedVehicles, UploadDocument,
)
from src.domains.vehicle.infrastructure.repositories import (
    SQLAlchemyVehicleRepository, SQLAlchemyVehicleDocumentRepository,
)

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


def _vread(v) -> VehicleRead:
    return VehicleRead(id=str(v.id), owner_id=str(v.owner_id), brand=v.brand, model=v.model,
                       year=v.year, license_plate=v.license_plate, color=v.color,
                       renavam=v.renavam, chassis=v.chassis, status=v.status,
                       daily_rate=v.daily_rate, description=v.description,
                       created_at=v.created_at, updated_at=v.updated_at)


def _dread(d) -> VehicleDocumentRead:
    return VehicleDocumentRead(id=str(d.id), vehicle_id=str(d.vehicle_id),
                               document_type=d.document_type, file_url=d.file_url,
                               is_approved=d.is_approved, created_at=d.created_at)


@router.post("/", response_model=VehicleRead, status_code=status.HTTP_201_CREATED)
async def register_vehicle(
    data: VehicleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = SQLAlchemyVehicleRepository(db)
    return _vread(await RegisterVehicle(repo).execute(current_user.id, data))


@router.get("/", response_model=list[VehicleRead])
async def list_vehicles(db: AsyncSession = Depends(get_db)):
    repo = SQLAlchemyVehicleRepository(db)
    return [_vread(v) for v in await ListApprovedVehicles(repo).execute()]


@router.get("/{vehicle_id}", response_model=VehicleRead)
async def get_vehicle(vehicle_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    repo = SQLAlchemyVehicleRepository(db)
    try:
        return _vread(await GetVehicle(repo).execute(vehicle_id))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.put("/{vehicle_id}", response_model=VehicleRead)
async def update_vehicle(
    vehicle_id: uuid.UUID,
    data: VehicleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = SQLAlchemyVehicleRepository(db)
    try:
        return _vread(await UpdateVehicle(repo).execute(vehicle_id, data))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post("/{vehicle_id}/approve", response_model=VehicleRead)
async def approve_vehicle(
    vehicle_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso restrito a administradores.")
    repo = SQLAlchemyVehicleRepository(db)
    try:
        return _vread(await ApproveVehicle(repo).execute(vehicle_id))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post("/{vehicle_id}/reject", response_model=VehicleRead)
async def reject_vehicle(
    vehicle_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso restrito a administradores.")
    repo = SQLAlchemyVehicleRepository(db)
    try:
        return _vread(await RejectVehicle(repo).execute(vehicle_id))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post("/{vehicle_id}/suspend", response_model=VehicleRead)
async def suspend_vehicle(
    vehicle_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso restrito a administradores.")
    repo = SQLAlchemyVehicleRepository(db)
    try:
        return _vread(await SuspendVehicle(repo).execute(vehicle_id))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post("/{vehicle_id}/documents", response_model=VehicleDocumentRead, status_code=status.HTTP_201_CREATED)
async def upload_document(
    vehicle_id: uuid.UUID,
    data: VehicleDocumentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    doc_repo = SQLAlchemyVehicleDocumentRepository(db)
    return _dread(await UploadDocument(doc_repo).execute(vehicle_id, data))


@router.get("/{vehicle_id}/documents", response_model=list[VehicleDocumentRead])
async def list_documents(
    vehicle_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    doc_repo = SQLAlchemyVehicleDocumentRepository(db)
    return [_dread(d) for d in await doc_repo.list_by_vehicle(vehicle_id)]
