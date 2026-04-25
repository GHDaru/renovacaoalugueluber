import uuid
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from enum import Enum

from src.shared.domain.base_entity import BaseEntity


class RentalStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


@dataclass
class Rental(BaseEntity):
    vehicle_id: uuid.UUID = field(default_factory=uuid.uuid4)
    renter_id: uuid.UUID = field(default_factory=uuid.uuid4)
    start_date: date = field(default_factory=date.today)
    end_date: date = field(default_factory=date.today)
    daily_rate: Decimal = Decimal("0.00")
    total_amount: Decimal = Decimal("0.00")
    status: RentalStatus = RentalStatus.PENDING
    notes: str = ""
