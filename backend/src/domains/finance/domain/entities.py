import uuid
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from enum import Enum

from src.shared.domain.base_entity import BaseEntity


class CostCategory(str, Enum):
    MAINTENANCE = "MAINTENANCE"
    INSURANCE = "INSURANCE"
    IPVA = "IPVA"
    LICENSING = "LICENSING"
    FUEL = "FUEL"
    CLEANING = "CLEANING"
    FINE = "FINE"
    OTHER = "OTHER"


@dataclass
class VehicleCost(BaseEntity):
    vehicle_id: uuid.UUID = field(default_factory=uuid.uuid4)
    category: CostCategory = CostCategory.OTHER
    description: str = ""
    amount: Decimal = Decimal("0.00")
    cost_date: date = field(default_factory=date.today)
    notes: str = ""


@dataclass
class FinancialSummary:
    vehicle_id: uuid.UUID
    total_revenue: Decimal
    total_costs: Decimal
    net_result: Decimal
    period_start: date
    period_end: date
