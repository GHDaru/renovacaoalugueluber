import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, Numeric, String, Boolean
from sqlalchemy.dialects.postgresql import UUID

from src.shared.infrastructure.database import Base


class VehicleModel(Base):
    __tablename__ = "vehicles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    license_plate = Column(String(10), nullable=False, unique=True)
    color = Column(String, nullable=False)
    renavam = Column(String, nullable=False)
    chassis = Column(String, nullable=False)
    status = Column(String, nullable=False, default="PENDING")
    daily_rate = Column(Numeric(10, 2), nullable=False, default=0)
    description = Column(String, nullable=False, default="")
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))


class VehicleDocumentModel(Base):
    __tablename__ = "vehicle_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    document_type = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    is_approved = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
