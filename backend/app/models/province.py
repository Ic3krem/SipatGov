from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Province(Base):
    __tablename__ = "provinces"

    id: Mapped[int] = mapped_column(primary_key=True)
    psgc_code: Mapped[str] = mapped_column(String(10), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"), index=True)

    region: Mapped["Region"] = relationship(back_populates="provinces")  # noqa: F821
    lgus: Mapped[list["LGU"]] = relationship(back_populates="province")  # noqa: F821
