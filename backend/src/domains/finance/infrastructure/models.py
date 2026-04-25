import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Column, Date, DateTime, Numeric, String
from sqlalchemy.dialects.postgresql import UUID

from src.shared.infrastructure.database import Base


class VehicleCostModel(Base):
    __tablename__ = "vehicle_costs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    category = Column(String, nullable=False, default="OTHER")
    description = Column(String, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    cost_date = Column(Date, nullable=False)
    notes = Column(String, nullable=False, default="")
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
