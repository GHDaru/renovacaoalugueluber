import uuid
from dataclasses import dataclass, field
from datetime import date

from src.shared.domain.base_entity import BaseEntity


@dataclass
class Renter(BaseEntity):
    user_id: uuid.UUID = field(default_factory=uuid.uuid4)
    full_name: str = ""
    cpf: str = ""
    cnh: str = ""
    cnh_category: str = ""
    cnh_expiry: date = field(default_factory=date.today)
    phone: str = ""
    address: str = ""
    is_verified: bool = False
