from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.rbac import get_current_user, require_roles
from app.deps import get_db
from app.models.enums import UserRole
from app.schemas.intake import IntakeDraftCreateIn, IntakeDraftFromAgentTextIn, IntakeDraftOut
from app.services.intake_service import IntakeService

router = APIRouter(prefix="/intake", tags=["intake"])


@router.post("/drafts", response_model=IntakeDraftOut, dependencies=[Depends(require_roles(UserRole.receptionist, UserRole.admin))])
def create_manual_intake_draft(payload: IntakeDraftCreateIn, db: Session = Depends(get_db), user=Depends(get_current_user)) -> IntakeDraftOut:
    draft = IntakeService.create_manual_draft(db, created_by_user_id=user.id, payload=payload.model_dump())
    draft = IntakeService.run_automation(db, draft=draft, preferred_specialty=None)
    return draft


@router.post("/drafts/from-agent-text", response_model=IntakeDraftOut, dependencies=[Depends(require_roles(UserRole.receptionist, UserRole.admin))])
def create_from_agent_text(payload: IntakeDraftFromAgentTextIn, db: Session = Depends(get_db), user=Depends(get_current_user)) -> IntakeDraftOut:
    draft = IntakeService.create_from_agent_text(db, created_by_user_id=user.id, transcript_text=payload.transcript_text)
    draft = IntakeService.run_automation(db, draft=draft, preferred_specialty=None)
    return draft


@router.get("/drafts/{draft_id}", response_model=IntakeDraftOut, dependencies=[Depends(require_roles(UserRole.receptionist, UserRole.doctor, UserRole.admin))])
def get_draft(draft_id: str, db: Session = Depends(get_db)) -> IntakeDraftOut:
    return IntakeService.get_draft(db, draft_id=draft_id)

