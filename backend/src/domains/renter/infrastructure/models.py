import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Column, Date, DateTime, String, Boolean
from sqlalchemy.dialects.postgresql import UUID

from src.shared.infrastructure.database import Base


class RenterModel(Base):
    __tablename__ = "renters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    full_name = Column(String, nullable=False)
    cpf = Column(String(11), nullable=False, unique=True)
    cnh = Column(String, nullable=False)
    cnh_category = Column(String, nullable=False)
    cnh_expiry = Column(Date, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=False)
    is_verified = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
