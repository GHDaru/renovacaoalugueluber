import uuid
from dataclasses import dataclass, field

from src.shared.domain.base_entity import BaseEntity


@dataclass
class Owner(BaseEntity):
    user_id: uuid.UUID = field(default_factory=uuid.uuid4)
    full_name: str = ""
    cpf: str = ""
    phone: str = ""
    address: str = ""
    is_verified: bool = False
