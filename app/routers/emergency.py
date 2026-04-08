from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.rbac import require_roles
from app.deps import get_db
from app.models.enums import UserRole
from app.schemas.emergency import EmergencyContentCreateIn, EmergencyContentOut
from app.services.emergency_service import EmergencyService

router = APIRouter(prefix="/emergency", tags=["emergency"])


@router.post("/content", response_model=EmergencyContentOut, dependencies=[Depends(require_roles(UserRole.receptionist, UserRole.doctor, UserRole.admin))])
def create_content(payload: EmergencyContentCreateIn, db: Session = Depends(get_db)) -> EmergencyContentOut:
    return EmergencyService.create_content(db, payload=payload.model_dump())


@router.get("/content", response_model=list[EmergencyContentOut])
def list_content(
    q: str | None = Query(default=None, description="Search by title."),
    kind: str | None = Query(default=None, description="Filter: video|text|first_aid"),
    db: Session = Depends(get_db),
) -> list[EmergencyContentOut]:
    # Public read: emergency help content should be reachable fast.
    return EmergencyService.list_content(db, q=q, kind=kind)


@router.get("/content/{content_id}", response_model=EmergencyContentOut)
def get_content(content_id: str, db: Session = Depends(get_db)) -> EmergencyContentOut:
    return EmergencyService.get_content(db, content_id=content_id)

