from pydantic import BaseModel, ConfigDict

from src.core import enums

__all__ = (
    "BelbinRoleRead",
    "BelbinCreate",
)


class BelbinRoleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: enums.BelbinRole
    percent: int
    points: int


class BelbinCreate(BaseModel):
    name: enums.BelbinRole
    percent: int
    points: int
