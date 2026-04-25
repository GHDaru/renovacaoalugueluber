from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class RenterCreate(BaseModel):
    full_name: str
    cpf: str
    cnh: str
    cnh_category: str
    cnh_expiry: date
    phone: str
    address: str


class RenterUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    cnh_expiry: Optional[date] = None


class RenterRead(BaseModel):
    id: str
    user_id: str
    full_name: str
    cpf: str
    cnh: str
    cnh_category: str
    cnh_expiry: date
    phone: str
    address: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
