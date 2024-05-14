from datetime import datetime

from pydantic import BaseModel


__all__ = (
    "CitizenshipRead",
    "MinimizedCitizenship"
)


class CitizenshipRead(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime

    name: str


class MinimizedCitizenship(BaseModel):
    id: int
    name: str