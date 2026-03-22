from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

REPORT_TYPES = ("concern", "feedback", "corruption_tip", "progress_update", "delay_report")
REPORT_STATUSES = ("submitted", "under_review", "verified", "resolved", "dismissed")


class CommunityReport(TimestampMixin, Base):
    __tablename__ = "community_reports"
    __table_args__ = (
        CheckConstraint(
            f"report_type IN ({', '.join(repr(s) for s in REPORT_TYPES)})",
            name="ck_reports_type",
        ),
        CheckConstraint(
            f"status IN ({', '.join(repr(s) for s in REPORT_STATUSES)})",
            name="ck_reports_status",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    lgu_id: Mapped[int] = mapped_column(ForeignKey("lgus.id"), index=True)
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"), index=True)
    title: Mapped[str] = mapped_column(String(300))
    description: Mapped[str] = mapped_column(Text)
    report_type: Mapped[str] = mapped_column(String(30), index=True)
    status: Mapped[str] = mapped_column(String(20), default="submitted", index=True)
    latitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 7))
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 7))
    address: Mapped[str | None] = mapped_column(Text)
    upvote_count: Mapped[int] = mapped_column(default=0)
    is_anonymous: Mapped[bool] = mapped_column(default=False)
    moderation_notes: Mapped[str | None] = mapped_column(Text)

    user: Mapped["User"] = relationship(back_populates="reports")  # noqa: F821
    lgu: Mapped["LGU"] = relationship(back_populates="community_reports")  # noqa: F821
    attachments: Mapped[list["ReportAttachment"]] = relationship(
        back_populates="report", cascade="all, delete-orphan"
    )
    upvotes: Mapped[list["ReportUpvote"]] = relationship(
        back_populates="report", cascade="all, delete-orphan"
    )


class ReportAttachment(TimestampMixin, Base):
    __tablename__ = "report_attachments"

    id: Mapped[int] = mapped_column(primary_key=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("community_reports.id", ondelete="CASCADE"), index=True)
    file_url: Mapped[str] = mapped_column(Text)
    file_type: Mapped[str | None] = mapped_column(String(20))
    thumbnail_url: Mapped[str | None] = mapped_column(Text)

    report: Mapped["CommunityReport"] = relationship(back_populates="attachments")


class ReportUpvote(Base):
    __tablename__ = "report_upvotes"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    report_id: Mapped[int] = mapped_column(
        ForeignKey("community_reports.id", ondelete="CASCADE"), primary_key=True
    )

    report: Mapped["CommunityReport"] = relationship(back_populates="upvotes")
