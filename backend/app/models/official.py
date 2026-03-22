from datetime import date

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Official(TimestampMixin, Base):
    __tablename__ = "officials"
    __table_args__ = (
        Index("idx_officials_current", "is_current", postgresql_where="is_current = true"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    lgu_id: Mapped[int] = mapped_column(ForeignKey("lgus.id"), index=True)
    full_name: Mapped[str] = mapped_column(String(200))
    position: Mapped[str] = mapped_column(String(100))
    party: Mapped[str | None] = mapped_column(String(100))
    term_start: Mapped[date | None]
    term_end: Mapped[date | None]
    is_current: Mapped[bool] = mapped_column(default=True)

    lgu: Mapped["LGU"] = relationship(back_populates="officials")  # noqa: F821
    promises: Mapped[list["Promise"]] = relationship(back_populates="official")  # noqa: F821
