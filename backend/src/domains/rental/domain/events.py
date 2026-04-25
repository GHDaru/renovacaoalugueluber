import uuid
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class RentalCreated:
    rental_id: uuid.UUID
    vehicle_id: uuid.UUID
    renter_id: uuid.UUID
    occurred_at: datetime = None

    def __post_init__(self):
        if self.occurred_at is None:
            self.occurred_at = datetime.now(timezone.utc)


@dataclass
class RentalActivated:
    rental_id: uuid.UUID
    occurred_at: datetime = None

    def __post_init__(self):
        if self.occurred_at is None:
            self.occurred_at = datetime.now(timezone.utc)


@dataclass
class RentalCompleted:
    rental_id: uuid.UUID
    occurred_at: datetime = None

    def __post_init__(self):
        if self.occurred_at is None:
            self.occurred_at = datetime.now(timezone.utc)


@dataclass
class RentalCancelled:
    rental_id: uuid.UUID
    occurred_at: datetime = None

    def __post_init__(self):
        if self.occurred_at is None:
            self.occurred_at = datetime.now(timezone.utc)
