from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.rbac import get_current_user, require_roles
from app.deps import get_db
from app.models.enums import UserRole
from app.schemas.patient import PatientProfileOut, PatientProfileUpdateIn
from app.services.patient_service import PatientService

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("/me/profile", response_model=PatientProfileOut, dependencies=[Depends(require_roles(UserRole.patient))])
def my_profile(db: Session = Depends(get_db), user=Depends(get_current_user)) -> PatientProfileOut:
    return PatientService.get_profile_for_user(db, user_id=user.id)


@router.patch("/me/profile", response_model=PatientProfileOut, dependencies=[Depends(require_roles(UserRole.patient))])
def update_my_profile(payload: PatientProfileUpdateIn, db: Session = Depends(get_db), user=Depends(get_current_user)) -> PatientProfileOut:
    patch = payload.model_dump(exclude_unset=True)
    return PatientService.update_profile(db, user_id=user.id, patch=patch)

