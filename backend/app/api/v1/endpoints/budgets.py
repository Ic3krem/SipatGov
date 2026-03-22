import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import BudgetAllocation

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("")
async def list_budgets(
    lgu_id: int | None = None,
    fiscal_year: int | None = None,
    category: str | None = Query(default=None, max_length=100),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """List budget allocations with filters."""
    try:
        query = select(BudgetAllocation)
        if lgu_id:
            query = query.where(BudgetAllocation.lgu_id == lgu_id)
        if fiscal_year:
            query = query.where(BudgetAllocation.fiscal_year == fiscal_year)
        if category:
            query = query.where(BudgetAllocation.category == category)
        query = query.order_by(BudgetAllocation.fiscal_year.desc()).limit(limit).offset(offset)
        result = await db.execute(query)
        return [
            {
                "id": b.id,
                "lgu_id": b.lgu_id,
                "fiscal_year": b.fiscal_year,
                "category": b.category,
                "subcategory": b.subcategory,
                "allocated_amount": float(b.allocated_amount),
                "released_amount": float(b.released_amount),
                "utilized_amount": float(b.utilized_amount),
            }
            for b in result.scalars().all()
        ]
    except SQLAlchemyError:
        logger.exception("Database error in list_budgets")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")


@router.get("/summary")
async def budget_summary(
    lgu_id: int = Query(ge=1),
    fiscal_year: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    """Aggregated budget summary for an LGU."""
    try:
        query = select(
            BudgetAllocation.category,
            func.sum(BudgetAllocation.allocated_amount).label("allocated"),
            func.sum(BudgetAllocation.released_amount).label("released"),
            func.sum(BudgetAllocation.utilized_amount).label("utilized"),
        ).where(BudgetAllocation.lgu_id == lgu_id)
        if fiscal_year:
            query = query.where(BudgetAllocation.fiscal_year == fiscal_year)
        query = query.group_by(BudgetAllocation.category)
        result = await db.execute(query)
        return [
            {
                "category": row.category,
                "allocated": float(row.allocated),
                "released": float(row.released),
                "utilized": float(row.utilized),
            }
            for row in result.all()
        ]
    except SQLAlchemyError:
        logger.exception("Database error in budget_summary")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")
