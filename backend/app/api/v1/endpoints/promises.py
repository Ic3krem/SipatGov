import logging

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Promise

logger = logging.getLogger(__name__)

router = APIRouter()

VALID_PROMISE_STATUSES = {
    "kept", "broken", "in_progress", "pending", "partially_kept", "unverifiable",
}


@router.get("")
async def list_promises(
    lgu_id: int | None = None,
    official_id: int | None = None,
    status: str | None = None,
    category: str | None = Query(default=None, max_length=100),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """List promises/commitments with filters."""
    if status and status not in VALID_PROMISE_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {', '.join(sorted(VALID_PROMISE_STATUSES))}",
        )
    try:
        query = select(Promise)
        if lgu_id:
            query = query.where(Promise.lgu_id == lgu_id)
        if official_id:
            query = query.where(Promise.official_id == official_id)
        if status:
            query = query.where(Promise.status == status)
        if category:
            query = query.where(Promise.category == category)
        query = query.order_by(Promise.updated_at.desc()).limit(limit).offset(offset)
        result = await db.execute(query)
        return [
            {
                "id": p.id,
                "official_id": p.official_id,
                "lgu_id": p.lgu_id,
                "title": p.title,
                "category": p.category,
                "status": p.status,
                "date_promised": str(p.date_promised) if p.date_promised else None,
                "deadline": str(p.deadline) if p.deadline else None,
                "confidence_score": float(p.confidence_score) if p.confidence_score else None,
            }
            for p in result.scalars().all()
        ]
    except SQLAlchemyError:
        logger.exception("Database error in list_promises")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")


@router.get("/stats")
async def promise_stats(
    lgu_id: int = Query(ge=1),
    db: AsyncSession = Depends(get_db),
):
    """Aggregate promise statistics for an LGU: kept/broken/pending counts."""
    try:
        result = await db.execute(
            select(Promise.status, func.count(Promise.id))
            .where(Promise.lgu_id == lgu_id)
            .group_by(Promise.status)
        )
        counts = {row[0]: row[1] for row in result.all()}
        total = sum(counts.values())
        return {
            "lgu_id": lgu_id,
            "total": total,
            "counts": counts,
            "percentages": {k: round(v / total * 100, 1) if total > 0 else 0 for k, v in counts.items()},
        }
    except SQLAlchemyError:
        logger.exception("Database error in promise_stats")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")


@router.get("/{promise_id}")
async def get_promise(
    promise_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
):
    """Get promise details with evidence chain."""
    try:
        result = await db.execute(select(Promise).where(Promise.id == promise_id))
        promise = result.scalar_one_or_none()
        if not promise:
            raise HTTPException(status_code=404, detail="Promise not found")
        return {
            "id": promise.id,
            "official_id": promise.official_id,
            "lgu_id": promise.lgu_id,
            "title": promise.title,
            "description": promise.description,
            "category": promise.category,
            "status": promise.status,
            "evidence_summary": promise.evidence_summary,
            "date_promised": str(promise.date_promised) if promise.date_promised else None,
            "deadline": str(promise.deadline) if promise.deadline else None,
            "verified_at": str(promise.verified_at) if promise.verified_at else None,
            "verified_by": promise.verified_by,
            "confidence_score": float(promise.confidence_score) if promise.confidence_score else None,
        }
    except HTTPException:
        raise
    except SQLAlchemyError:
        logger.exception("Database error in get_promise")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")
