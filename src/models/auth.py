from datetime import datetime

from sqlalchemy import ForeignKey, String, Text, Enum, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core import db, enums

__all__ = (
    "User",
    "RefreshToken",
    "AccessTokenAPI",
)


class User(db.TimeStampMixin):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str] = mapped_column(Text())
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=False)
    is_verified_email: Mapped[bool] = mapped_column(default=False)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    middle_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(100))
    password_changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    search_status: Mapped[enums.SearchStatus] = mapped_column(Enum(enums.SearchStatus))
    search_region: Mapped[str | None] = mapped_column(String(255), nullable=True)


class RefreshToken(db.TimeStampMixin):
    __tablename__ = "refresh_token"

    token: Mapped[str] = mapped_column(String(), unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship()


class AccessTokenAPI(db.TimeStampMixin):
    __tablename__ = "access_token_api"

    token: Mapped[str] = mapped_column(String(100), unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship()
