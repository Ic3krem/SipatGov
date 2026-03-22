import logging

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import LGU, BudgetAllocation, Project, Promise

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("")
async def list_lgus(
    region_id: int | None = None,
    province_id: int | None = None,
    lgu_type: str | None = None,
    search: str | None = Query(default=None, max_length=100),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """List LGUs with optional filters."""
    try:
        query = select(LGU)
        if region_id:
            query = query.where(LGU.region_id == region_id)
        if province_id:
            query = query.where(LGU.province_id == province_id)
        if lgu_type:
            query = query.where(LGU.lgu_type == lgu_type)
        if search:
            query = query.where(LGU.name.ilike(f"%{search}%"))
        query = query.order_by(LGU.name).limit(limit).offset(offset)
        result = await db.execute(query)
        return [
            {
                "id": l.id,
                "psgc_code": l.psgc_code,
                "name": l.name,
                "lgu_type": l.lgu_type,
                "latitude": float(l.latitude) if l.latitude else None,
                "longitude": float(l.longitude) if l.longitude else None,
                "transparency_score": float(l.transparency_score),
            }
            for l in result.scalars().all()
        ]
    except SQLAlchemyError:
        logger.exception("Database error in list_lgus")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")


@router.get("/map")
async def lgus_for_map(db: AsyncSession = Depends(get_db)):
    """Lightweight LGU data optimized for map markers."""
    try:
        result = await db.execute(
            select(
                LGU.id, LGU.name, LGU.latitude, LGU.longitude,
                LGU.transparency_score, LGU.lgu_type,
            ).where(LGU.latitude.isnot(None))
        )
        return [
            {
                "id": row.id,
                "name": row.name,
                "lat": float(row.latitude),
                "lng": float(row.longitude),
                "score": float(row.transparency_score),
                "type": row.lgu_type,
            }
            for row in result.all()
        ]
    except SQLAlchemyError:
        logger.exception("Database error in lgus_for_map")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")


@router.get("/{lgu_id}")
async def get_lgu(
    lgu_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
):
    """Get LGU details."""
    try:
        result = await db.execute(select(LGU).where(LGU.id == lgu_id))
        lgu = result.scalar_one_or_none()
        if not lgu:
            raise HTTPException(status_code=404, detail="LGU not found")
        return {
            "id": lgu.id,
            "psgc_code": lgu.psgc_code,
            "name": lgu.name,
            "lgu_type": lgu.lgu_type,
            "latitude": float(lgu.latitude) if lgu.latitude else None,
            "longitude": float(lgu.longitude) if lgu.longitude else None,
            "population": lgu.population,
            "income_class": lgu.income_class,
            "transparency_score": float(lgu.transparency_score),
        }
    except HTTPException:
        raise
    except SQLAlchemyError:
        logger.exception("Database error in get_lgu")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")


@router.get("/{lgu_id}/summary")
async def get_lgu_summary(
    lgu_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
):
    """Dashboard summary for an LGU: budget totals, project counts, promise stats."""
    try:
        # Budget totals for current year
        budget_result = await db.execute(
            select(
                func.sum(BudgetAllocation.allocated_amount).label("total_allocated"),
                func.sum(BudgetAllocation.utilized_amount).label("total_utilized"),
            ).where(BudgetAllocation.lgu_id == lgu_id, BudgetAllocation.fiscal_year == 2026)
        )
        budget = budget_result.one()

        # Project counts by status
        project_result = await db.execute(
            select(Project.status, func.count(Project.id))
            .where(Project.lgu_id == lgu_id)
            .group_by(Project.status)
        )
        project_counts = {row[0]: row[1] for row in project_result.all()}

        # Promise stats
        promise_result = await db.execute(
            select(Promise.status, func.count(Promise.id))
            .where(Promise.lgu_id == lgu_id)
            .group_by(Promise.status)
        )
        promise_counts = {row[0]: row[1] for row in promise_result.all()}

        return {
            "lgu_id": lgu_id,
            "budget": {
                "total_allocated": float(budget.total_allocated or 0),
                "total_utilized": float(budget.total_utilized or 0),
            },
            "projects": project_counts,
            "promises": promise_counts,
        }
    except SQLAlchemyError:
        logger.exception("Database error in get_lgu_summary")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")
