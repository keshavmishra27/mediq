from __future__ import annotations

from datetime import date

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.models.doctor import DoctorProfile
from app.models.enums import AmbulanceStatus, BedStatus
from app.models.hospital import Bed, ReferralHospital


class AssignmentService:
    """
    Encapsulates the "automation logic" for allocating resources.

    This is intentionally simple (MVP-ready) but structured so you can expand:
    - shift-based scheduling for doctors
    - bed types (ICU, general, oxygen) and triage rules
    - rules engine / AI scoring later
    """

    @staticmethod
    def assign_bed_if_available(db: Session) -> Bed | None:
        bed = db.scalar(select(Bed).where(Bed.status == BedStatus.available).order_by(Bed.ward.asc(), Bed.bed_number.asc()).limit(1))
        if not bed:
            return None
        bed.status = BedStatus.occupied
        db.add(bed)
        db.flush()
        return bed

    @staticmethod
    def assign_doctor_if_available(db: Session, *, preferred_specialty: str | None = None) -> DoctorProfile | None:
        q = select(DoctorProfile).where(DoctorProfile.is_available.is_(True))
        if preferred_specialty:
            q = q.where(DoctorProfile.specialty.ilike(f"%{preferred_specialty}%"))
        doctor = db.scalar(q.order_by(DoctorProfile.updated_at.asc()).limit(1))
        if not doctor:
            return None
        doctor.is_available = False  # simplistic locking: mark busy
        db.add(doctor)
        db.flush()
        return doctor

    @staticmethod
    def referral_suggestions(db: Session, *, reason: str) -> list[dict]:
        # For MVP: return the first few referral hospitals.
        hospitals = db.scalars(select(ReferralHospital).order_by(ReferralHospital.name.asc()).limit(5)).all()
        return [
            {"hospital_id": h.id, "name": h.name, "phone": h.phone, "address": h.address, "reason": reason}
            for h in hospitals
        ]

