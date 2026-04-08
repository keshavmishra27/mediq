from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.patient import PatientProfile
from app.models.user import User


class PatientService:
    @staticmethod
    def get_profile_for_user(db: Session, *, user_id: str) -> PatientProfile:
        profile = db.scalar(select(PatientProfile).where(PatientProfile.user_id == user_id))
        if not profile:
            raise HTTPException(status_code=404, detail="Patient profile not found")
        return profile

    @staticmethod
    def update_profile(db: Session, *, user_id: str, patch: dict) -> PatientProfile:
        profile = PatientService.get_profile_for_user(db, user_id=user_id)
        for k, v in patch.items():
            setattr(profile, k, v)
        db.add(profile)
        db.flush()
        return profile

