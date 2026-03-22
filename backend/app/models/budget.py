from decimal import Decimal

from sqlalchemy import ForeignKey, Index, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class BudgetAllocation(TimestampMixin, Base):
    __tablename__ = "budget_allocations"
    __table_args__ = (
        UniqueConstraint("lgu_id", "fiscal_year", "category", "subcategory", name="uq_budget"),
        Index("idx_budget_lgu_year", "lgu_id", "fiscal_year"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    lgu_id: Mapped[int] = mapped_column(ForeignKey("lgus.id"))
    fiscal_year: Mapped[int]
    category: Mapped[str] = mapped_column(String(100), index=True)
    subcategory: Mapped[str | None] = mapped_column(String(150))
    allocated_amount: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    released_amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=0)
    utilized_amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=0)
    source_document_id: Mapped[int | None] = mapped_column(ForeignKey("documents.id"))

    lgu: Mapped["LGU"] = relationship(back_populates="budget_allocations")  # noqa: F821
    source_document: Mapped["Document | None"] = relationship()  # noqa: F821
