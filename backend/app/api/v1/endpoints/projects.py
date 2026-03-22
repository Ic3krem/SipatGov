import logging

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Project

logger = logging.getLogger(__name__)

router = APIRouter()

VALID_PROJECT_STATUSES = {
    "planned", "ongoing", "completed", "delayed", "cancelled", "suspended",
}


@router.get("")
async def list_projects(
    lgu_id: int | None = None,
    status: str | None = None,
    category: str | None = Query(default=None, max_length=100),
    fiscal_year: int | None = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """List projects with filters."""
    if status and status not in VALID_PROJECT_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {', '.join(sorted(VALID_PROJECT_STATUSES))}",
        )
    try:
        query = select(Project)
        if lgu_id:
            query = query.where(Project.lgu_id == lgu_id)
        if status:
            query = query.where(Project.status == status)
        if category:
            query = query.where(Project.category == category)
        if fiscal_year:
            query = query.where(Project.fiscal_year == fiscal_year)
        query = query.order_by(Project.updated_at.desc()).limit(limit).offset(offset)
        result = await db.execute(query)
        return [
            {
                "id": p.id,
                "lgu_id": p.lgu_id,
                "title": p.title,
                "category": p.category,
                "status": p.status,
                "approved_budget": float(p.approved_budget) if p.approved_budget else None,
                "contract_amount": float(p.contract_amount) if p.contract_amount else None,
                "latitude": float(p.latitude) if p.latitude else None,
                "longitude": float(p.longitude) if p.longitude else None,
                "philgeps_ref": p.philgeps_ref,
                "fiscal_year": p.fiscal_year,
            }
            for p in result.scalars().all()
        ]
    except SQLAlchemyError:
        logger.exception("Database error in list_projects")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")


@router.get("/map")
async def projects_geojson(
    status: str | None = None,
    category: str | None = Query(default=None, max_length=100),
    db: AsyncSession = Depends(get_db),
):
    """GeoJSON feature collection for map rendering."""
    if status and status not in VALID_PROJECT_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {', '.join(sorted(VALID_PROJECT_STATUSES))}",
        )
    try:
        query = select(Project).where(Project.latitude.isnot(None))
        if status:
            query = query.where(Project.status == status)
        if category:
            query = query.where(Project.category == category)
        result = await db.execute(query)
        features = [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(p.longitude), float(p.latitude)],
                },
                "properties": {
                    "id": p.id,
                    "title": p.title,
                    "status": p.status,
                    "category": p.category,
                    "budget": float(p.approved_budget) if p.approved_budget else None,
                },
            }
            for p in result.scalars().all()
        ]
        return {"type": "FeatureCollection", "features": features}
    except SQLAlchemyError:
        logger.exception("Database error in projects_geojson")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")


@router.get("/{project_id}")
async def get_project(
    project_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
):
    """Get project details."""
    try:
        result = await db.execute(select(Project).where(Project.id == project_id))
        project = result.scalar_one_or_none()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return {
            "id": project.id,
            "lgu_id": project.lgu_id,
            "title": project.title,
            "description": project.description,
            "category": project.category,
            "status": project.status,
            "contractor": project.contractor,
            "approved_budget": float(project.approved_budget) if project.approved_budget else None,
            "contract_amount": float(project.contract_amount) if project.contract_amount else None,
            "actual_cost": float(project.actual_cost) if project.actual_cost else None,
            "start_date": str(project.start_date) if project.start_date else None,
            "target_end_date": str(project.target_end_date) if project.target_end_date else None,
            "actual_end_date": str(project.actual_end_date) if project.actual_end_date else None,
            "latitude": float(project.latitude) if project.latitude else None,
            "longitude": float(project.longitude) if project.longitude else None,
            "address": project.address,
            "philgeps_ref": project.philgeps_ref,
            "fiscal_year": project.fiscal_year,
        }
    except HTTPException:
        raise
    except SQLAlchemyError:
        logger.exception("Database error in get_project")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")
