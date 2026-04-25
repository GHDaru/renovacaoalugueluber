import uuid
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from src.shared.domain.base_entity import BaseEntity


class VehicleStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    SUSPENDED = "SUSPENDED"


@dataclass
class Vehicle(BaseEntity):
    owner_id: uuid.UUID = field(default_factory=uuid.uuid4)
    brand: str = ""
    model: str = ""
    year: int = 0
    license_plate: str = ""
    color: str = ""
    renavam: str = ""
    chassis: str = ""
    status: VehicleStatus = VehicleStatus.PENDING
    daily_rate: Decimal = Decimal("0.00")
    description: str = ""


@dataclass
class VehicleDocument(BaseEntity):
    vehicle_id: uuid.UUID = field(default_factory=uuid.uuid4)
    document_type: str = ""
    file_url: str = ""
    is_approved: bool = False
