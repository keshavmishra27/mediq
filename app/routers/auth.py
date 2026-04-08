from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.rbac import get_current_user, require_roles
from app.deps import get_db
from app.models.enums import UserRole
from app.schemas.auth import LoginIn, RegisterPatientIn, RegisterStaffIn, Token, UserOut
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
def register_patient(payload: RegisterPatientIn, db: Session = Depends(get_db)) -> UserOut:
    user = AuthService.register_patient(
        db,
        login_id=payload.login_id,
        password=payload.password,
        email=str(payload.email) if payload.email else None,
        phone=payload.phone,
        full_name=payload.full_name,
    )
    return user


@router.post("/register-staff", response_model=UserOut, dependencies=[Depends(require_roles(UserRole.admin))])
def register_staff(payload: RegisterStaffIn, db: Session = Depends(get_db)) -> UserOut:
    user = AuthService.register_staff(
        db,
        role=payload.role,
        login_id=payload.login_id,
        password=payload.password,
        email=str(payload.email) if payload.email else None,
        phone=payload.phone,
        full_name=payload.full_name,
        specialty=payload.specialty,
    )
    return user


@router.post("/login", response_model=Token)
def login(payload: LoginIn, db: Session = Depends(get_db)) -> Token:
    token = AuthService.login(db, login_id=payload.login_id, password=payload.password)
    return Token(access_token=token)


@router.get("/me", response_model=UserOut)
def me(user=Depends(get_current_user)) -> UserOut:
    return user

