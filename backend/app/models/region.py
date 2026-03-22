from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Region(Base):
    __tablename__ = "regions"

    id: Mapped[int] = mapped_column(primary_key=True)
    psgc_code: Mapped[str] = mapped_column(String(10), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    region_code: Mapped[str] = mapped_column(String(20))

    provinces: Mapped[list["Province"]] = relationship(back_populates="region")  # noqa: F821
    lgus: Mapped[list["LGU"]] = relationship(back_populates="region")  # noqa: F821
