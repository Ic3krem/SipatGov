from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Document

router = APIRouter()


@router.get("")
async def list_documents(
    source: str | None = None,
    lgu_id: int | None = None,
    document_type: str | None = None,
    processing_status: str | None = None,
    limit: int = Query(default=50, le=200),
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """List crawled documents with filters."""
    query = select(Document)
    if source:
        query = query.where(Document.source_portal == source)
    if lgu_id:
        query = query.where(Document.lgu_id == lgu_id)
    if document_type:
        query = query.where(Document.document_type == document_type)
    if processing_status:
        query = query.where(Document.processing_status == processing_status)
    query = query.order_by(Document.crawled_at.desc()).limit(limit).offset(offset)
    result = await db.execute(query)
    return [
        {
            "id": d.id,
            "source_portal": d.source_portal,
            "title": d.title,
            "document_type": d.document_type,
            "lgu_id": d.lgu_id,
            "processing_status": d.processing_status,
            "crawled_at": str(d.crawled_at) if d.crawled_at else None,
        }
        for d in result.scalars().all()
    ]


@router.get("/{document_id}")
async def get_document(document_id: int, db: AsyncSession = Depends(get_db)):
    """Get document details with extracted structured data."""
    result = await db.execute(select(Document).where(Document.id == document_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return {
        "id": doc.id,
        "source_portal": doc.source_portal,
        "source_url": doc.source_url,
        "title": doc.title,
        "document_type": doc.document_type,
        "lgu_id": doc.lgu_id,
        "processing_status": doc.processing_status,
        "structured_data": doc.structured_data,
        "crawled_at": str(doc.crawled_at) if doc.crawled_at else None,
        "processed_at": str(doc.processed_at) if doc.processed_at else None,
    }
