from datetime import date
from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Index, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

PROJECT_STATUSES = (
    "planned", "bidding", "awarded", "ongoing", "completed", "delayed", "cancelled", "suspended"
)


class Project(TimestampMixin, Base):
    __tablename__ = "projects"
    __table_args__ = (
        CheckConstraint(
            f"status IN ({', '.join(repr(s) for s in PROJECT_STATUSES)})",
            name="ck_projects_status",
        ),
        Index("idx_projects_coords", "latitude", "longitude"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    lgu_id: Mapped[int] = mapped_column(ForeignKey("lgus.id"), index=True)
    title: Mapped[str] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(30), default="planned", index=True)
    contractor: Mapped[str | None] = mapped_column(String(300))
    approved_budget: Mapped[Decimal | None] = mapped_column(Numeric(18, 2))
    contract_amount: Mapped[Decimal | None] = mapped_column(Numeric(18, 2))
    actual_cost: Mapped[Decimal | None] = mapped_column(Numeric(18, 2))
    start_date: Mapped[date | None]
    target_end_date: Mapped[date | None]
    actual_end_date: Mapped[date | None]
    latitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 7))
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 7))
    address: Mapped[str | None] = mapped_column(Text)
    philgeps_ref: Mapped[str | None] = mapped_column(String(50), index=True)
    source_document_id: Mapped[int | None] = mapped_column(ForeignKey("documents.id"))
    fiscal_year: Mapped[int | None] = mapped_column(index=True)

    lgu: Mapped["LGU"] = relationship(back_populates="projects")  # noqa: F821
    source_document: Mapped["Document | None"] = relationship()  # noqa: F821
