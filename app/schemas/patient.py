from __future__ import annotations

from datetime import date

from pydantic import Field

from app.schemas.common import APIModel


class PatientProfileOut(APIModel):
    id: str
    user_id: str
    full_name: str
    dob: date | None = None
    gender: str | None = None
    address: str | None = None
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None


class PatientProfileUpdateIn(APIModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=255)
    dob: date | None = None
    gender: str | None = None
    address: str | None = None
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None

