from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber

from src.core import enums

__all__ = (
    "UserRead",
    "UserCreate",
    "UserUpdate",
    "UserUpdateAdmin",

    "BaseUserUpdate",
)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_verified: bool
    is_verified_email: bool

    first_name: str
    last_name: str
    phone_number: str
    search_status: enums.SearchStatus

    created_at: datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    phone_number: PhoneNumber

    first_name: str
    last_name: str


class BaseUserUpdate(BaseModel):
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    password: str | None = Field(default=None)
    email: EmailStr | None = Field(default=None)
    search_status: enums.SearchStatus | None = Field(default=None)


class UserUpdate(BaseUserUpdate):
    pass


class UserUpdateAdmin(BaseUserUpdate):
    is_active: bool | None = Field(default=None)
    is_superuser: bool | None = Field(default=None)
    is_verified: bool | None = Field(default=None)
    is_verified_email: bool | None = Field(default=None)
