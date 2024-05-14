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


class IPhoneNumber(PhoneNumber):
    phone_format: str = 'E164'


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
    middle_name: str | None
    phone_number: IPhoneNumber
    search_status: enums.SearchStatus
    search_region: str | None

    password_changed_at: datetime
    created_at: datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    phone_number: IPhoneNumber

    first_name: str
    last_name: str
    middle_name: str | None


class BaseUserUpdate(BaseModel):
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    middle_name: str | None = Field(default=None)
    password: str | None = Field(default=None)
    email: EmailStr | None = Field(default=None)
    search_status: enums.SearchStatus | None = Field(default=None)
    phone_number: IPhoneNumber | None = Field(default=None)
    search_region: str | None = Field(default=None)


class UserUpdate(BaseUserUpdate):
    pass


class UserUpdateAdmin(BaseUserUpdate):
    is_active: bool | None = Field(default=None)
    is_superuser: bool | None = Field(default=None)
    is_verified: bool | None = Field(default=None)
    is_verified_email: bool | None = Field(default=None)
