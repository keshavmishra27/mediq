from __future__ import annotations

from datetime import datetime

from pydantic import Field

from app.models.enums import AppointmentStatus, VisitType
from app.schemas.common import APIModel


class AppointmentCreateIn(APIModel):
    scheduled_for: datetime
    visit_type: VisitType
    requested_location: str | None = None
    reason: str | None = None
    preferred_specialty: str | None = Field(default=None, description="Helps auto-assign a doctor.")


class AppointmentOut(APIModel):
    id: str
    patient_id: str
    doctor_id: str | None = None
    scheduled_for: datetime
    visit_type: VisitType
    requested_location: str | None = None
    reason: str | None = None
    status: AppointmentStatus


class ConsultationCreateIn(APIModel):
    appointment_id: str | None = None
    patient_id: str
    notes: str | None = None
    vitals: dict | None = None
    prescriptions: dict | None = None


class ConsultationOut(APIModel):
    id: str
    appointment_id: str | None = None
    patient_id: str
    doctor_id: str
    notes: str | None = None
    vitals: dict | None = None
    prescriptions: dict | None = None
    created_at: datetime


class ReportCreateIn(APIModel):
    patient_id: str
    title: str = Field(min_length=2, max_length=255)
    content: dict


class ReportOut(APIModel):
    id: str
    patient_id: str
    title: str
    content: dict
    pdf_url: str | None = None
    created_at: datetime

