from __future__ import annotations

from datetime import date

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import BedStatus
from app.models.hospital import Ambulance, Bed, Medicine, ReferralHospital


class HospitalService:
    # Beds
    @staticmethod
    def create_bed(db: Session, *, ward: str, bed_number: str, status: BedStatus) -> Bed:
        bed = Bed(ward=ward, bed_number=bed_number, status=status)
        db.add(bed)
        db.flush()
        return bed

    @staticmethod
    def list_beds(db: Session) -> list[Bed]:
        return db.scalars(select(Bed).order_by(Bed.ward.asc(), Bed.bed_number.asc())).all()

    @staticmethod
    def update_bed(db: Session, *, bed_id: str, patch: dict) -> Bed:
        bed = db.get(Bed, bed_id)
        if not bed:
            raise HTTPException(status_code=404, detail="Bed not found")
        for k, v in patch.items():
            setattr(bed, k, v)
        db.add(bed)
        db.flush()
        return bed

    # Ambulances
    @staticmethod
    def create_ambulance(db: Session, *, code: str, status, current_location: str | None) -> Ambulance:
        amb = Ambulance(code=code, status=status, current_location=current_location)
        db.add(amb)
        db.flush()
        return amb

    @staticmethod
    def list_ambulances(db: Session) -> list[Ambulance]:
        return db.scalars(select(Ambulance).order_by(Ambulance.code.asc())).all()

    @staticmethod
    def update_ambulance(db: Session, *, ambulance_id: str, patch: dict) -> Ambulance:
        amb = db.get(Ambulance, ambulance_id)
        if not amb:
            raise HTTPException(status_code=404, detail="Ambulance not found")
        for k, v in patch.items():
            setattr(amb, k, v)
        db.add(amb)
        db.flush()
        return amb

    # Medicines
    @staticmethod
    def create_medicine(db: Session, *, payload: dict) -> Medicine:
        med = Medicine(**payload)
        db.add(med)
        db.flush()
        return med

    @staticmethod
    def list_medicines(db: Session) -> list[Medicine]:
        return db.scalars(select(Medicine).order_by(Medicine.name.asc())).all()

    @staticmethod
    def low_stock_alerts(db: Session) -> list[dict]:
        meds = db.scalars(select(Medicine)).all()
        out = []
        for m in meds:
            if m.quantity <= m.low_stock_threshold:
                out.append({"medicine_id": m.id, "name": m.name, "quantity": m.quantity, "threshold": m.low_stock_threshold})
        return out

    @staticmethod
    def expired_medicines(db: Session, *, today: date | None = None) -> list[dict]:
        today = today or date.today()
        meds = db.scalars(select(Medicine).where(Medicine.expiry_date.is_not(None))).all()
        return [{"medicine_id": m.id, "name": m.name, "expiry_date": m.expiry_date} for m in meds if m.expiry_date and m.expiry_date <= today]

    @staticmethod
    def update_medicine(db: Session, *, medicine_id: str, patch: dict) -> Medicine:
        med = db.get(Medicine, medicine_id)
        if not med:
            raise HTTPException(status_code=404, detail="Medicine not found")
        for k, v in patch.items():
            setattr(med, k, v)
        db.add(med)
        db.flush()
        return med

    # Referral hospitals
    @staticmethod
    def create_referral_hospital(db: Session, *, payload: dict) -> ReferralHospital:
        h = ReferralHospital(**payload)
        db.add(h)
        db.flush()
        return h

    @staticmethod
    def list_referral_hospitals(db: Session) -> list[ReferralHospital]:
        return db.scalars(select(ReferralHospital).order_by(ReferralHospital.name.asc())).all()

