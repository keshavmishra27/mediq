from __future__ import annotations

from pydantic import Field

from app.models.enums import IntakeStatus
from app.schemas.common import APIModel


class IntakeDraftCreateIn(APIModel):
    patient_name: str | None = Field(default=None, max_length=255)
    patient_phone: str | None = Field(default=None, max_length=32)
    patient_age: int | None = Field(default=None, ge=0, le=130)
    symptoms: str | None = None
    pickup_location: str | None = None


class IntakeDraftFromAgentTextIn(APIModel):
    transcript_text: str = Field(min_length=10, description="Text produced from speech-to-text.")


class IntakeDraftOut(APIModel):
    id: str
    status: IntakeStatus
    patient_name: str | None = None
    patient_phone: str | None = None
    patient_age: int | None = None
    symptoms: str | None = None
    pickup_location: str | None = None
    extracted_fields: dict | None = None
    assigned_bed_id: str | None = None
    assigned_doctor_id: str | None = None
    referral_suggestions: list[dict] | None = None

