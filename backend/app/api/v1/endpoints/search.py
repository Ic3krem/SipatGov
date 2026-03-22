from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_, select, union_all
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import LGU, Project, Promise

router = APIRouter()


@router.get("")
async def search(
    q: str = Query(min_length=2),
    lgu_id: int | None = None,
    limit: int = Query(default=20, le=50),
    db: AsyncSession = Depends(get_db),
):
    """Full-text search across projects, promises, and LGUs."""
    search_term = f"%{q}%"
    results = []

    # Search LGUs
    lgu_query = select(LGU.id, LGU.name).where(LGU.name.ilike(search_term)).limit(limit)
    lgu_result = await db.execute(lgu_query)
    for row in lgu_result.all():
        results.append({"type": "lgu", "id": row.id, "title": row.name})

    # Search Projects
    proj_query = select(Project.id, Project.title).where(
        Project.title.ilike(search_term)
    )
    if lgu_id:
        proj_query = proj_query.where(Project.lgu_id == lgu_id)
    proj_query = proj_query.limit(limit)
    proj_result = await db.execute(proj_query)
    for row in proj_result.all():
        results.append({"type": "project", "id": row.id, "title": row.title})

    # Search Promises
    prom_query = select(Promise.id, Promise.title).where(
        Promise.title.ilike(search_term)
    )
    if lgu_id:
        prom_query = prom_query.where(Promise.lgu_id == lgu_id)
    prom_query = prom_query.limit(limit)
    prom_result = await db.execute(prom_query)
    for row in prom_result.all():
        results.append({"type": "promise", "id": row.id, "title": row.title})

    return {"query": q, "results": results[:limit]}
