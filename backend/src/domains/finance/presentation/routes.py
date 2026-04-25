import uuid
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.database import get_db
from src.domains.auth.application.security import get_current_user
from src.domains.auth.domain.entities import User, UserRole
from src.domains.finance.application.dtos import (
    FinancialSummaryRead, VehicleCostCreate, VehicleCostRead, VehicleCostUpdate,
)
from src.domains.finance.application.use_cases import (
    DeleteCost, GetCostsByVehicle, GetFinancialSummary, RegisterCost, UpdateCost,
)
from src.domains.finance.infrastructure.repositories import SQLAlchemyVehicleCostRepository
from src.domains.rental.infrastructure.repositories import SQLAlchemyRentalRepository

router = APIRouter(prefix="/finance", tags=["finance"])


def _require_admin(current_user: User) -> None:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso restrito a administradores.")


def _cread(c) -> VehicleCostRead:
    return VehicleCostRead(
        id=str(c.id), vehicle_id=str(c.vehicle_id), category=c.category,
        description=c.description, amount=c.amount, cost_date=c.cost_date,
        notes=c.notes, created_at=c.created_at, updated_at=c.updated_at,
    )


@router.post("/costs", response_model=VehicleCostRead, status_code=status.HTTP_201_CREATED)
async def register_cost(
    data: VehicleCostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _require_admin(current_user)
    repo = SQLAlchemyVehicleCostRepository(db)
    return _cread(await RegisterCost(repo).execute(data))


@router.get("/costs", response_model=list[VehicleCostRead])
async def list_costs(
    vehicle_id: Optional[uuid.UUID] = Query(default=None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _require_admin(current_user)
    repo = SQLAlchemyVehicleCostRepository(db)
    if vehicle_id:
        costs = await GetCostsByVehicle(repo).execute(vehicle_id)
    else:
        costs = await repo.list_all()
    return [_cread(c) for c in costs]


@router.get("/costs/{cost_id}", response_model=VehicleCostRead)
async def get_cost(
    cost_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _require_admin(current_user)
    repo = SQLAlchemyVehicleCostRepository(db)
    cost = await repo.get_by_id(cost_id)
    if not cost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Custo não encontrado.")
    return _cread(cost)


@router.put("/costs/{cost_id}", response_model=VehicleCostRead)
async def update_cost(
    cost_id: uuid.UUID,
    data: VehicleCostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _require_admin(current_user)
    repo = SQLAlchemyVehicleCostRepository(db)
    try:
        return _cread(await UpdateCost(repo).execute(cost_id, data))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.delete("/costs/{cost_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cost(
    cost_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _require_admin(current_user)
    repo = SQLAlchemyVehicleCostRepository(db)
    try:
        await DeleteCost(repo).execute(cost_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get("/summary/{vehicle_id}", response_model=FinancialSummaryRead)
async def get_vehicle_summary(
    vehicle_id: uuid.UUID,
    period_start: date = Query(...),
    period_end: date = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _require_admin(current_user)
    cost_repo = SQLAlchemyVehicleCostRepository(db)
    rental_repo = SQLAlchemyRentalRepository(db)
    summary = await GetFinancialSummary(cost_repo, rental_repo).execute(vehicle_id, period_start, period_end)
    return FinancialSummaryRead(
        vehicle_id=str(summary.vehicle_id), total_revenue=summary.total_revenue,
        total_costs=summary.total_costs, net_result=summary.net_result,
        period_start=summary.period_start, period_end=summary.period_end,
    )


@router.get("/summary", response_model=list[FinancialSummaryRead])
async def get_all_summaries(
    period_start: date = Query(...),
    period_end: date = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _require_admin(current_user)
    cost_repo = SQLAlchemyVehicleCostRepository(db)
    rental_repo = SQLAlchemyRentalRepository(db)
    all_costs = await cost_repo.list_all()
    vehicle_ids = list({c.vehicle_id for c in all_costs})
    use_case = GetFinancialSummary(cost_repo, rental_repo)
    summaries = []
    for vid in vehicle_ids:
        s = await use_case.execute(vid, period_start, period_end)
        summaries.append(FinancialSummaryRead(
            vehicle_id=str(s.vehicle_id), total_revenue=s.total_revenue,
            total_costs=s.total_costs, net_result=s.net_result,
            period_start=s.period_start, period_end=s.period_end,
        ))
    return summaries
