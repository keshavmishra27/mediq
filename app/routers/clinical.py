from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from app.core.rbac import get_current_user, require_roles
from app.deps import get_db
from app.models.enums import UserRole
from app.schemas.clinical import (
    AppointmentCreateIn,
    AppointmentOut,
    ConsultationCreateIn,
    ConsultationOut,
    ReportCreateIn,
    ReportOut,
)
from app.services.clinical_service import ClinicalService
from app.services.patient_service import PatientService

router = APIRouter(prefix="/clinical", tags=["clinical"])


@router.post("/appointments", response_model=AppointmentOut, dependencies=[Depends(require_roles(UserRole.patient))])
def create_appointment(payload: AppointmentCreateIn, db: Session = Depends(get_db), user=Depends(get_current_user)) -> AppointmentOut:
    patient = PatientService.get_profile_for_user(db, user_id=user.id)
    appt = ClinicalService.create_appointment(
        db,
        patient_id=patient.id,
        scheduled_for=payload.scheduled_for,
        visit_type=payload.visit_type,
        requested_location=payload.requested_location,
        reason=payload.reason,
        preferred_specialty=payload.preferred_specialty,
    )
    return appt


@router.get("/appointments/me", response_model=list[AppointmentOut], dependencies=[Depends(require_roles(UserRole.patient))])
def list_my_appointments(db: Session = Depends(get_db), user=Depends(get_current_user)) -> list[AppointmentOut]:
    patient = PatientService.get_profile_for_user(db, user_id=user.id)
    return ClinicalService.list_patient_appointments(db, patient_id=patient.id)


@router.post("/consultations", response_model=ConsultationOut, dependencies=[Depends(require_roles(UserRole.doctor))])
def create_consultation(payload: ConsultationCreateIn, db: Session = Depends(get_db), user=Depends(get_current_user)) -> ConsultationOut:
    # doctor_id = current doctor's profile id
    doctor_profile_id = user.doctor_profile.id if user.doctor_profile else None
    if not doctor_profile_id:
        # Defensive: user role says doctor, but profile missing.
        raise ValueError("Doctor profile missing")

    c = ClinicalService.create_consultation(
        db,
        doctor_id=doctor_profile_id,
        patient_id=payload.patient_id,
        appointment_id=payload.appointment_id,
        notes=payload.notes,
        vitals=payload.vitals,
        prescriptions=payload.prescriptions,
    )
    return c


@router.get("/consultations/me", response_model=list[ConsultationOut], dependencies=[Depends(require_roles(UserRole.patient))])
def list_my_consultations(db: Session = Depends(get_db), user=Depends(get_current_user)) -> list[ConsultationOut]:
    patient = PatientService.get_profile_for_user(db, user_id=user.id)
    return ClinicalService.list_patient_consultations(db, patient_id=patient.id)


def _fake_generate_pdf(report_id: str) -> None:
    """
    Background task placeholder.

    In production you'd render a PDF and upload to object storage.
    """

    _ = report_id


@router.post("/reports", response_model=ReportOut, dependencies=[Depends(require_roles(UserRole.doctor, UserRole.receptionist, UserRole.admin))])
def create_report(
    payload: ReportCreateIn,
    background: BackgroundTasks,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
) -> ReportOut:
    r = ClinicalService.create_report(db, created_by_user_id=user.id, patient_id=payload.patient_id, title=payload.title, content=payload.content)
    background.add_task(_fake_generate_pdf, r.id)
    return r


@router.get("/reports/{patient_id}", response_model=list[ReportOut], dependencies=[Depends(require_roles(UserRole.patient, UserRole.doctor, UserRole.receptionist, UserRole.admin))])
def list_patient_reports(patient_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)) -> list[ReportOut]:
    # Simple access policy:
    # - patients can only read their own
    # - staff can read any
    if user.role == UserRole.patient:
        my_profile = PatientService.get_profile_for_user(db, user_id=user.id)
        if my_profile.id != patient_id:
            return []  # intentionally not leaking existence
    return ClinicalService.list_patient_reports(db, patient_id=patient_id)

