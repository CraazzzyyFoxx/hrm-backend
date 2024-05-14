from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.core import enums

__all__ = (
    "BelbinRoleRead",
    "BelbinCreate",
    "BelbinRoleEntityRead"
)


class BelbinRoleEntityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime | None

    role_id: int
    name: enums.BelbinRole
    percent: int
    points: int


class BelbinRoleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime | None

    user_id: int
    roles: list[BelbinRoleEntityRead]


class BelbinCreate(BaseModel):
    name: enums.BelbinRole
    percent: int
    points: int
