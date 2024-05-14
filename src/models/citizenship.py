from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.core import db


__all__ = (
    "Citizenship",
)


class Citizenship(db.TimeStampMixin):
    __tablename__ = "citizenship"

    name: Mapped[str] = mapped_column(String(255))
