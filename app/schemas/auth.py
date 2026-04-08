from __future__ import annotations

from pydantic import EmailStr, Field

from app.models.enums import UserRole
from app.schemas.common import APIModel


class Token(APIModel):
    access_token: str
    token_type: str = "bearer"


class RegisterPatientIn(APIModel):
    login_id: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=8, max_length=128)
    email: EmailStr | None = None
    phone: str | None = None
    full_name: str = Field(min_length=2, max_length=255)


class RegisterStaffIn(APIModel):
    """
    Admin-only: create receptionist/doctor/admin accounts.
    """

    role: UserRole
    login_id: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=8, max_length=128)
    email: EmailStr | None = None
    phone: str | None = None
    full_name: str = Field(min_length=2, max_length=255)
    specialty: str | None = None  # only used if role=doctor


class LoginIn(APIModel):
    login_id: str
    password: str


class UserOut(APIModel):
    id: str
    role: UserRole
    login_id: str
    email: EmailStr | None = None
    phone: str | None = None
    is_active: bool

