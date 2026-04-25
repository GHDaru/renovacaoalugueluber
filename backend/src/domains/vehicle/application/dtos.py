from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from src.domains.vehicle.domain.entities import VehicleStatus


class VehicleCreate(BaseModel):
    brand: str
    model: str
    year: int
    license_plate: str
    color: str
    renavam: str
    chassis: str
    daily_rate: Decimal
    description: str = ""


class VehicleUpdate(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    color: Optional[str] = None
    daily_rate: Optional[Decimal] = None
    description: Optional[str] = None


class VehicleRead(BaseModel):
    id: str
    owner_id: str
    brand: str
    model: str
    year: int
    license_plate: str
    color: str
    renavam: str
    chassis: str
    status: VehicleStatus
    daily_rate: Decimal
    description: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class VehicleDocumentCreate(BaseModel):
    document_type: str
    file_url: str


class VehicleDocumentRead(BaseModel):
    id: str
    vehicle_id: str
    document_type: str
    file_url: str
    is_approved: bool
    created_at: datetime

    model_config = {"from_attributes": True}
