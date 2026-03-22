from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class ScrapingScheduleModel(Base):
    """SQLAlchemy model for the scraping_schedules table."""

    __tablename__ = "scraping_schedules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    spider_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    cron_expression: Mapped[str] = mapped_column(String(50), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    last_run_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_status: Mapped[str | None] = mapped_column(String(20))
    items_scraped: Mapped[int] = mapped_column(Integer, default=0)
    avg_quality_score: Mapped[Decimal] = mapped_column(
        Numeric(3, 2), default=Decimal("0.00")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
