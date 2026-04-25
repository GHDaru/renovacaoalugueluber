from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from src.domains.rental.domain.entities import RentalStatus


class RentalCreate(BaseModel):
    vehicle_id: str
    start_date: date
    end_date: date
    daily_rate: Decimal
    notes: str = ""


class RentalRead(BaseModel):
    id: str
    vehicle_id: str
    renter_id: str
    start_date: date
    end_date: date
    daily_rate: Decimal
    total_amount: Decimal
    status: RentalStatus
    notes: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
