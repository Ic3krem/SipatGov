import logging

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import CommunityReport
from app.schemas.report import CreateReportRequest

logger = logging.getLogger(__name__)

router = APIRouter()

VALID_REPORT_SORTS = {"newest", "popular"}
VALID_REPORT_STATUSES = {"submitted", "under_review", "verified", "resolved", "dismissed"}
VALID_REPORT_TYPES = {"concern", "feedback", "corruption_tip", "progress_update", "delay_report"}


@router.get("")
async def list_reports(
    lgu_id: int | None = None,
    project_id: int | None = None,
    report_type: str | None = None,
    status: str | None = None,
    sort: str = "newest",
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """List community reports with filters."""
    if sort not in VALID_REPORT_SORTS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort. Must be one of: {', '.join(sorted(VALID_REPORT_SORTS))}",
        )
    if report_type and report_type not in VALID_REPORT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid report_type. Must be one of: {', '.join(sorted(VALID_REPORT_TYPES))}",
        )
    if status and status not in VALID_REPORT_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {', '.join(sorted(VALID_REPORT_STATUSES))}",
        )
    try:
        query = select(CommunityReport)
        if lgu_id:
            query = query.where(CommunityReport.lgu_id == lgu_id)
        if project_id:
            query = query.where(CommunityReport.project_id == project_id)
        if report_type:
            query = query.where(CommunityReport.report_type == report_type)
        if status:
            query = query.where(CommunityReport.status == status)
        if sort == "popular":
            query = query.order_by(CommunityReport.upvote_count.desc())
        else:
            query = query.order_by(CommunityReport.created_at.desc())
        query = query.limit(limit).offset(offset)
        result = await db.execute(query)
        return [
            {
                "id": r.id,
                "lgu_id": r.lgu_id,
                "project_id": r.project_id,
                "title": r.title,
                "report_type": r.report_type,
                "status": r.status,
                "upvote_count": r.upvote_count,
                "is_anonymous": r.is_anonymous,
                "created_at": str(r.created_at),
            }
            for r in result.scalars().all()
        ]
    except SQLAlchemyError:
        logger.exception("Database error in list_reports")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")


@router.post("")
async def create_report(
    report_data: CreateReportRequest,
    db: AsyncSession = Depends(get_db),
):
    """Submit a new community report (auth required)."""
    # TODO: implement with auth - validate user from JWT
    return {"message": "create report endpoint - TODO: implement with auth"}


@router.get("/{report_id}")
async def get_report(
    report_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
):
    """Get report details."""
    try:
        result = await db.execute(select(CommunityReport).where(CommunityReport.id == report_id))
        report = result.scalar_one_or_none()
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        return {
            "id": report.id,
            "user_id": report.user_id if not report.is_anonymous else None,
            "lgu_id": report.lgu_id,
            "project_id": report.project_id,
            "title": report.title,
            "description": report.description,
            "report_type": report.report_type,
            "status": report.status,
            "latitude": float(report.latitude) if report.latitude else None,
            "longitude": float(report.longitude) if report.longitude else None,
            "address": report.address,
            "upvote_count": report.upvote_count,
            "is_anonymous": report.is_anonymous,
            "created_at": str(report.created_at),
        }
    except HTTPException:
        raise
    except SQLAlchemyError:
        logger.exception("Database error in get_report")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")


@router.post("/{report_id}/upvote")
async def upvote_report(
    report_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
):
    """Upvote a community report (auth required)."""
    return {"message": "upvote endpoint - TODO: implement with auth"}


@router.delete("/{report_id}/upvote")
async def remove_upvote(
    report_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
):
    """Remove upvote from a report (auth required)."""
    return {"message": "remove upvote endpoint - TODO: implement with auth"}
