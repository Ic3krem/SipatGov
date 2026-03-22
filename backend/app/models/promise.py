from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

PROMISE_STATUSES = ("kept", "broken", "in_progress", "pending", "partially_kept", "unverifiable")


class Promise(TimestampMixin, Base):
    __tablename__ = "promises"
    __table_args__ = (
        CheckConstraint(
            f"status IN ({', '.join(repr(s) for s in PROMISE_STATUSES)})",
            name="ck_promises_status",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    official_id: Mapped[int | None] = mapped_column(ForeignKey("officials.id"), index=True)
    lgu_id: Mapped[int] = mapped_column(ForeignKey("lgus.id"), index=True)
    title: Mapped[str] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)
    evidence_summary: Mapped[str | None] = mapped_column(Text)
    date_promised: Mapped[date | None]
    deadline: Mapped[date | None]
    verified_at: Mapped[datetime | None]
    verified_by: Mapped[str | None] = mapped_column(String(100))
    confidence_score: Mapped[Decimal | None] = mapped_column(Numeric(3, 2))
    source_document_id: Mapped[int | None] = mapped_column(ForeignKey("documents.id"))

    official: Mapped["Official | None"] = relationship(back_populates="promises")  # noqa: F821
    lgu: Mapped["LGU"] = relationship(back_populates="promises")  # noqa: F821
    source_document: Mapped["Document | None"] = relationship()  # noqa: F821
    evidence_items: Mapped[list["PromiseEvidence"]] = relationship(
        back_populates="promise", cascade="all, delete-orphan"
    )


class PromiseEvidence(TimestampMixin, Base):
    __tablename__ = "promise_evidence"
    __table_args__ = (
        CheckConstraint(
            "evidence_type IN ('project', 'document', 'budget', 'report', 'external_link')",
            name="ck_evidence_type",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    promise_id: Mapped[int] = mapped_column(ForeignKey("promises.id", ondelete="CASCADE"), index=True)
    evidence_type: Mapped[str] = mapped_column(String(30))
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"))
    document_id: Mapped[int | None] = mapped_column(ForeignKey("documents.id"))
    budget_id: Mapped[int | None] = mapped_column(ForeignKey("budget_allocations.id"))
    report_id: Mapped[int | None] = mapped_column(ForeignKey("community_reports.id"))
    external_url: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)

    promise: Mapped["Promise"] = relationship(back_populates="evidence_items")
