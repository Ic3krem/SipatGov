from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Index, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class LGU(TimestampMixin, Base):
    __tablename__ = "lgus"
    __table_args__ = (
        CheckConstraint(
            "lgu_type IN ('municipality', 'city', 'province', 'barangay')",
            name="ck_lgus_type",
        ),
        Index("idx_lgus_coords", "latitude", "longitude"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    psgc_code: Mapped[str] = mapped_column(String(10), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(150))
    lgu_type: Mapped[str] = mapped_column(String(20), index=True)
    province_id: Mapped[int | None] = mapped_column(ForeignKey("provinces.id"), index=True)
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"), index=True)
    latitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 7))
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 7))
    population: Mapped[int | None]
    income_class: Mapped[str | None] = mapped_column(String(10))
    transparency_score: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=0)

    region: Mapped["Region"] = relationship(back_populates="lgus")  # noqa: F821
    province: Mapped["Province | None"] = relationship(back_populates="lgus")  # noqa: F821
    officials: Mapped[list["Official"]] = relationship(back_populates="lgu")  # noqa: F821
    projects: Mapped[list["Project"]] = relationship(back_populates="lgu")  # noqa: F821
    promises: Mapped[list["Promise"]] = relationship(back_populates="lgu")  # noqa: F821
    budget_allocations: Mapped[list["BudgetAllocation"]] = relationship(back_populates="lgu")  # noqa: F821
    documents: Mapped[list["Document"]] = relationship(back_populates="lgu")  # noqa: F821
    community_reports: Mapped[list["CommunityReport"]] = relationship(back_populates="lgu")  # noqa: F821
