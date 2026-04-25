import uuid
from datetime import date, datetime, timezone
from decimal import Decimal

from src.domains.finance.domain.entities import VehicleCost, FinancialSummary
from src.domains.finance.domain.repositories import IVehicleCostRepository
from src.domains.finance.application.dtos import VehicleCostCreate, VehicleCostUpdate
from src.domains.rental.domain.repositories import IRentalRepository


class RegisterCost:
    def __init__(self, repo: IVehicleCostRepository) -> None:
        self._repo = repo

    async def execute(self, data: VehicleCostCreate) -> VehicleCost:
        cost = VehicleCost(
            vehicle_id=uuid.UUID(data.vehicle_id),
            category=data.category,
            description=data.description,
            amount=data.amount,
            cost_date=data.cost_date,
            notes=data.notes,
        )
        return await self._repo.save(cost)


class GetCostsByVehicle:
    def __init__(self, repo: IVehicleCostRepository) -> None:
        self._repo = repo

    async def execute(self, vehicle_id: uuid.UUID) -> list[VehicleCost]:
        return await self._repo.list_by_vehicle(vehicle_id)


class UpdateCost:
    def __init__(self, repo: IVehicleCostRepository) -> None:
        self._repo = repo

    async def execute(self, cost_id: uuid.UUID, data: VehicleCostUpdate) -> VehicleCost:
        cost = await self._repo.get_by_id(cost_id)
        if not cost:
            raise ValueError("Custo não encontrado.")
        if data.category is not None:
            cost.category = data.category
        if data.description is not None:
            cost.description = data.description
        if data.amount is not None:
            cost.amount = data.amount
        if data.cost_date is not None:
            cost.cost_date = data.cost_date
        if data.notes is not None:
            cost.notes = data.notes
        cost.updated_at = datetime.now(timezone.utc)
        return await self._repo.save(cost)


class DeleteCost:
    def __init__(self, repo: IVehicleCostRepository) -> None:
        self._repo = repo

    async def execute(self, cost_id: uuid.UUID) -> None:
        cost = await self._repo.get_by_id(cost_id)
        if not cost:
            raise ValueError("Custo não encontrado.")
        await self._repo.delete(cost_id)


class GetFinancialSummary:
    def __init__(self, cost_repo: IVehicleCostRepository, rental_repo: IRentalRepository) -> None:
        self._cost_repo = cost_repo
        self._rental_repo = rental_repo

    async def execute(self, vehicle_id: uuid.UUID, period_start: date, period_end: date) -> FinancialSummary:
        costs = await self._cost_repo.list_by_vehicle_and_period(vehicle_id, period_start, period_end)
        total_costs = sum((c.amount for c in costs), Decimal("0.00"))

        rentals = await self._rental_repo.list_completed_by_vehicle_and_period(
            vehicle_id, period_start, period_end
        )
        total_revenue = sum((r.total_amount for r in rentals), Decimal("0.00"))

        return FinancialSummary(
            vehicle_id=vehicle_id,
            total_revenue=total_revenue,
            total_costs=total_costs,
            net_result=total_revenue - total_costs,
            period_start=period_start,
            period_end=period_end,
        )
