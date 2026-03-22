from sqlalchemy import CheckConstraint, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("role IN ('citizen', 'moderator', 'admin')", name="ck_users_role"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str | None] = mapped_column(String(255), unique=True)
    phone: Mapped[str | None] = mapped_column(String(20), unique=True)
    display_name: Mapped[str | None] = mapped_column(String(100))
    password_hash: Mapped[str | None] = mapped_column(String(255))
    avatar_url: Mapped[str | None] = mapped_column(Text)
    home_lgu_id: Mapped[int | None] = mapped_column(ForeignKey("lgus.id"), index=True)
    home_region_id: Mapped[int | None] = mapped_column(ForeignKey("regions.id"))
    role: Mapped[str] = mapped_column(String(20), default="citizen")
    is_verified: Mapped[bool] = mapped_column(default=False)
    onboarding_completed: Mapped[bool] = mapped_column(default=False)
    supabase_uid: Mapped[str | None] = mapped_column(String(36), unique=True)

    reports: Mapped[list["CommunityReport"]] = relationship(back_populates="user")  # noqa: F821
