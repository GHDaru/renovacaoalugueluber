import uuid
from dataclasses import dataclass, field
from enum import Enum

from src.shared.domain.base_entity import BaseEntity


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    OWNER = "OWNER"
    RENTER = "RENTER"


@dataclass
class User(BaseEntity):
    email: str = ""
    hashed_password: str = ""
    full_name: str = ""
    role: UserRole = UserRole.RENTER
    is_active: bool = True
