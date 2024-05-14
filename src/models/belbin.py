from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core import db, enums
from src.models.auth import User

__all__ = (
    "BelbinRole", "BelbinRoleEntity"
)


class BelbinRole(db.TimeStampMixin):
    __tablename__ = "belbin_role"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship()
    roles: Mapped[list["BelbinRoleEntity"]] = relationship()


class BelbinRoleEntity(db.TimeStampMixin):
    __tablename__ = "belbin_role_entity"

    role_id: Mapped[int] = mapped_column(ForeignKey("belbin_role.id", ondelete="CASCADE"))
    role: Mapped["BelbinRole"] = relationship(back_populates="roles")
    name: Mapped[enums.BelbinRole] = mapped_column(Enum(enums.BelbinRole))
    percent: Mapped[int] = mapped_column()
    points: Mapped[int] = mapped_column()
