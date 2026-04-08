from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.clinical import Appointment, Consultation, Report
from app.models.doctor import DoctorProfile
from app.models.enums import AppointmentStatus
from app.models.patient import PatientProfile
from app.services.assignment_service import AssignmentService


class ClinicalService:
    @staticmethod
    def create_appointment(
        db: Session,
        *,
        patient_id: str,
        scheduled_for,
        visit_type,
        requested_location: str | None,
        reason: str | None,
        preferred_specialty: str | None,
    ) -> Appointment:
        # Auto-assign a doctor if possible; otherwise appointment is still created in requested state.
        doctor = AssignmentService.assign_doctor_if_available(db, preferred_specialty=preferred_specialty)

        appt = Appointment(
            patient_id=patient_id,
            doctor_id=doctor.id if doctor else None,
            scheduled_for=scheduled_for,
            visit_type=visit_type,
            requested_location=requested_location,
            reason=reason,
            status=AppointmentStatus.confirmed if doctor else AppointmentStatus.requested,
        )
        db.add(appt)
        db.flush()
        return appt

    @staticmethod
    def list_patient_appointments(db: Session, *, patient_id: str) -> list[Appointment]:
        return db.scalars(select(Appointment).where(Appointment.patient_id == patient_id).order_by(Appointment.scheduled_for.desc())).all()

    @staticmethod
    def create_consultation(
        db: Session, *, doctor_id: str, patient_id: str, appointment_id: str | None, notes: str | None, vitals: dict | None, prescriptions: dict | None
    ) -> Consultation:
        # Ensure doctor/patient exist (helps return consistent 404s).
        if not db.get(DoctorProfile, doctor_id):
            raise HTTPException(status_code=404, detail="Doctor not found")
        if not db.get(PatientProfile, patient_id):
            raise HTTPException(status_code=404, detail="Patient not found")

        c = Consultation(
            doctor_id=doctor_id,
            patient_id=patient_id,
            appointment_id=appointment_id,
            notes=notes,
            vitals=vitals,
            prescriptions=prescriptions,
        )
        db.add(c)
        db.flush()
        return c

    @staticmethod
    def list_patient_consultations(db: Session, *, patient_id: str) -> list[Consultation]:
        return db.scalars(select(Consultation).where(Consultation.patient_id == patient_id).order_by(Consultation.created_at.desc())).all()

    @staticmethod
    def create_report(db: Session, *, created_by_user_id: str, patient_id: str, title: str, content: dict) -> Report:
        if not db.get(PatientProfile, patient_id):
            raise HTTPException(status_code=404, detail="Patient not found")
        r = Report(patient_id=patient_id, created_by_user_id=created_by_user_id, title=title, content=content, pdf_url=None)
        db.add(r)
        db.flush()
        return r

    @staticmethod
    def list_patient_reports(db: Session, *, patient_id: str) -> list[Report]:
        return db.scalars(select(Report).where(Report.patient_id == patient_id).order_by(Report.created_at.desc())).all()

