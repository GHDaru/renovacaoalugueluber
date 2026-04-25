from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from src.domains.finance.domain.entities import CostCategory


class VehicleCostCreate(BaseModel):
    vehicle_id: str
    category: CostCategory
    description: str
    amount: Decimal
    cost_date: date
    notes: str = ""


class VehicleCostUpdate(BaseModel):
    category: Optional[CostCategory] = None
    description: Optional[str] = None
    amount: Optional[Decimal] = None
    cost_date: Optional[date] = None
    notes: Optional[str] = None


class VehicleCostRead(BaseModel):
    id: str
    vehicle_id: str
    category: CostCategory
    description: str
    amount: Decimal
    cost_date: date
    notes: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class FinancialSummaryRead(BaseModel):
    vehicle_id: str
    total_revenue: Decimal
    total_costs: Decimal
    net_result: Decimal
    period_start: date
    period_end: date
