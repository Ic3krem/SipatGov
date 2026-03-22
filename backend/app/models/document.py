from datetime import datetime

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

SOURCE_PORTALS = ("philgeps", "dbm", "coa", "efoi", "manual")
PROCESSING_STATUSES = ("pending", "downloading", "ocr_processing", "nlp_processing", "completed", "failed")


class Document(TimestampMixin, Base):
    __tablename__ = "documents"
    __table_args__ = (
        CheckConstraint(
            f"source_portal IN ({', '.join(repr(s) for s in SOURCE_PORTALS)})",
            name="ck_docs_source_portal",
        ),
        CheckConstraint(
            f"processing_status IN ({', '.join(repr(s) for s in PROCESSING_STATUSES)})",
            name="ck_docs_processing_status",
        ),
        Index("idx_docs_hash", "file_hash", unique=True, postgresql_where="file_hash IS NOT NULL"),
        Index("idx_docs_structured", "structured_data", postgresql_using="gin"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    source_portal: Mapped[str] = mapped_column(String(50), index=True)
    source_url: Mapped[str] = mapped_column(Text)
    title: Mapped[str | None] = mapped_column(String(500))
    document_type: Mapped[str | None] = mapped_column(String(50))
    lgu_id: Mapped[int | None] = mapped_column(ForeignKey("lgus.id"), index=True)
    file_path: Mapped[str | None] = mapped_column(Text)
    file_hash: Mapped[str | None] = mapped_column(String(64))
    raw_text: Mapped[str | None] = mapped_column(Text)
    structured_data: Mapped[dict | None] = mapped_column(JSONB)
    processing_status: Mapped[str] = mapped_column(String(20), default="pending", index=True)
    processing_error: Mapped[str | None] = mapped_column(Text)
    crawled_at: Mapped[datetime | None]
    processed_at: Mapped[datetime | None]

    lgu: Mapped["LGU | None"] = relationship(back_populates="documents")  # noqa: F821
