from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import LGU, Province, Region

router = APIRouter()


@router.get("")
async def list_regions(db: AsyncSession = Depends(get_db)):
    """List all Philippine regions."""
    result = await db.execute(select(Region).order_by(Region.region_code))
    regions = result.scalars().all()
    return [
        {"id": r.id, "psgc_code": r.psgc_code, "name": r.name, "region_code": r.region_code}
        for r in regions
    ]


@router.get("/{region_id}/provinces")
async def list_provinces(region_id: int, db: AsyncSession = Depends(get_db)):
    """List provinces in a region."""
    result = await db.execute(
        select(Province).where(Province.region_id == region_id).order_by(Province.name)
    )
    provinces = result.scalars().all()
    return [
        {"id": p.id, "psgc_code": p.psgc_code, "name": p.name, "region_id": p.region_id}
        for p in provinces
    ]


@router.get("/provinces/{province_id}/lgus")
async def list_lgus_by_province(province_id: int, db: AsyncSession = Depends(get_db)):
    """List LGUs in a province."""
    result = await db.execute(
        select(LGU).where(LGU.province_id == province_id).order_by(LGU.name)
    )
    lgus = result.scalars().all()
    return [
        {
            "id": l.id,
            "psgc_code": l.psgc_code,
            "name": l.name,
            "lgu_type": l.lgu_type,
        }
        for l in lgus
    ]
