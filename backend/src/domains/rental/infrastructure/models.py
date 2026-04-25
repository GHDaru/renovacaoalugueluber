import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Column, Date, DateTime, Numeric, String
from sqlalchemy.dialects.postgresql import UUID

from src.shared.infrastructure.database import Base


class RentalModel(Base):
    __tablename__ = "rentals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    renter_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    daily_rate = Column(Numeric(10, 2), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String, nullable=False, default="PENDING")
    notes = Column(String, nullable=False, default="")
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
