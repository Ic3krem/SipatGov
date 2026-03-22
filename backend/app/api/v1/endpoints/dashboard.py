import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import BudgetAllocation, CommunityReport, LGU, Project, Promise

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("")
async def get_dashboard(
    lgu_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    """Home dashboard data for user's home LGU (or national overview)."""
    if lgu_id:
        return await _lgu_dashboard(lgu_id, db)
    return await _national_dashboard(db)


async def _lgu_dashboard(lgu_id: int, db: AsyncSession):
    """Dashboard data for a specific LGU."""
    try:
        # LGU info
        lgu_result = await db.execute(select(LGU).where(LGU.id == lgu_id))
        lgu = lgu_result.scalar_one_or_none()
        if not lgu:
            raise HTTPException(status_code=404, detail="LGU not found")

        # Budget summary (current year)
        budget_result = await db.execute(
            select(
                func.sum(BudgetAllocation.allocated_amount),
                func.sum(BudgetAllocation.utilized_amount),
            ).where(BudgetAllocation.lgu_id == lgu_id, BudgetAllocation.fiscal_year == 2026)
        )
        budget = budget_result.one()

        # Project counts
        project_result = await db.execute(
            select(func.count(Project.id)).where(Project.lgu_id == lgu_id)
        )
        total_projects = project_result.scalar() or 0

        # Promise stats
        promise_result = await db.execute(
            select(Promise.status, func.count(Promise.id))
            .where(Promise.lgu_id == lgu_id)
            .group_by(Promise.status)
        )
        promise_counts = {row[0]: row[1] for row in promise_result.all()}

        # Recent reports count
        report_count_result = await db.execute(
            select(func.count(CommunityReport.id)).where(CommunityReport.lgu_id == lgu_id)
        )
        total_reports = report_count_result.scalar() or 0

        return {
            "lgu": {"id": lgu.id, "name": lgu.name, "transparency_score": float(lgu.transparency_score)},
            "budget": {
                "total_allocated": float(budget[0] or 0),
                "total_utilized": float(budget[1] or 0),
            },
            "total_projects": total_projects,
            "promises": promise_counts,
            "total_reports": total_reports,
        }
    except HTTPException:
        raise
    except SQLAlchemyError:
        logger.exception("Database error in _lgu_dashboard")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")


async def _national_dashboard(db: AsyncSession):
    """National-level aggregated dashboard."""
    try:
        lgu_count = await db.execute(select(func.count(LGU.id)))
        project_count = await db.execute(select(func.count(Project.id)))
        promise_count = await db.execute(select(func.count(Promise.id)))
        report_count = await db.execute(select(func.count(CommunityReport.id)))

        return {
            "total_lgus": lgu_count.scalar() or 0,
            "total_projects": project_count.scalar() or 0,
            "total_promises": promise_count.scalar() or 0,
            "total_reports": report_count.scalar() or 0,
        }
    except SQLAlchemyError:
        logger.exception("Database error in _national_dashboard")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")


@router.get("/national")
async def national_dashboard(db: AsyncSession = Depends(get_db)):
    """National-level aggregation endpoint."""
    return await _national_dashboard(db)
