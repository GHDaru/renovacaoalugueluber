from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class OwnerCreate(BaseModel):
    full_name: str
    cpf: str
    phone: str
    address: str


class OwnerUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class OwnerRead(BaseModel):
    id: str
    user_id: str
    full_name: str
    cpf: str
    phone: str
    address: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
