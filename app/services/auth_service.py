from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.doctor import DoctorProfile
from app.models.enums import UserRole
from app.models.patient import PatientProfile
from app.models.user import User


class AuthService:
    @staticmethod
    def register_patient(db: Session, *, login_id: str, password: str, email: str | None, phone: str | None, full_name: str) -> User:
        existing = db.scalar(select(User).where(User.login_id == login_id))
        if existing:
            raise HTTPException(status_code=400, detail="login_id already exists")

        if email:
            existing_email = db.scalar(select(User).where(User.email == email))
            if existing_email:
                raise HTTPException(status_code=400, detail="email already exists")

        user = User(
            role=UserRole.patient,
            login_id=login_id,
            email=email,
            phone=phone,
            password_hash=hash_password(password),
            is_active=True,
        )
        db.add(user)
        db.flush()  # get user.id for FK

        profile = PatientProfile(user_id=user.id, full_name=full_name)
        db.add(profile)
        db.flush()
        return user

    @staticmethod
    def register_staff(
        db: Session,
        *,
        role: UserRole,
        login_id: str,
        password: str,
        email: str | None,
        phone: str | None,
        full_name: str,
        specialty: str | None = None,
    ) -> User:
        if role == UserRole.patient:
            raise HTTPException(status_code=400, detail="Use patient registration for patient accounts")

        existing = db.scalar(select(User).where(User.login_id == login_id))
        if existing:
            raise HTTPException(status_code=400, detail="login_id already exists")

        user = User(
            role=role,
            login_id=login_id,
            email=email,
            phone=phone,
            password_hash=hash_password(password),
            is_active=True,
        )
        db.add(user)
        db.flush()

        if role == UserRole.doctor:
            db.add(DoctorProfile(user_id=user.id, full_name=full_name, specialty=specialty, is_available=True))

        return user

    @staticmethod
    def login(db: Session, *, login_id: str, password: str) -> str:
        user = db.scalar(select(User).where(User.login_id == login_id))
        if not user or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        if not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        token = create_access_token(subject=user.id, claims={"role": user.role.value, "login_id": user.login_id})
        return token

