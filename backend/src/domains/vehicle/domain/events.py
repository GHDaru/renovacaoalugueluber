import uuid
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class VehicleRegistered:
    vehicle_id: uuid.UUID
    owner_id: uuid.UUID
    occurred_at: datetime = None

    def __post_init__(self):
        if self.occurred_at is None:
            self.occurred_at = datetime.now(timezone.utc)


@dataclass
class VehicleApproved:
    vehicle_id: uuid.UUID
    occurred_at: datetime = None

    def __post_init__(self):
        if self.occurred_at is None:
            self.occurred_at = datetime.now(timezone.utc)


@dataclass
class VehicleRejected:
    vehicle_id: uuid.UUID
    reason: str = ""
    occurred_at: datetime = None

    def __post_init__(self):
        if self.occurred_at is None:
            self.occurred_at = datetime.now(timezone.utc)
