from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.enums import IntakeStatus
from app.models.intake import IntakeDraft
from app.services.agent_intake_parser import AgentIntakeParser
from app.services.assignment_service import AssignmentService


class IntakeService:
    @staticmethod
    def create_manual_draft(db: Session, *, created_by_user_id: str | None, payload: dict) -> IntakeDraft:
        draft = IntakeDraft(created_by_user_id=created_by_user_id, **payload)
        db.add(draft)
        db.flush()
        return draft

    @staticmethod
    def create_from_agent_text(db: Session, *, created_by_user_id: str | None, transcript_text: str) -> IntakeDraft:
        extracted = AgentIntakeParser.extract(transcript_text)
        draft = IntakeDraft(
            created_by_user_id=created_by_user_id,
            raw_agent_text=transcript_text,
            extracted_fields=extracted,
            patient_name=extracted.get("patient_name"),
            patient_phone=extracted.get("patient_phone"),
            patient_age=extracted.get("patient_age"),
            symptoms=extracted.get("symptoms"),
            pickup_location=extracted.get("pickup_location"),
        )
        db.add(draft)
        db.flush()
        return draft

    @staticmethod
    def run_automation(db: Session, *, draft: IntakeDraft, preferred_specialty: str | None = None) -> IntakeDraft:
        """
        The core USP workflow:
        - Assign bed if available.
        - Assign doctor if available.
        - If not possible, generate referral suggestions.
        """

        bed = AssignmentService.assign_bed_if_available(db)
        doctor = AssignmentService.assign_doctor_if_available(db, preferred_specialty=preferred_specialty)

        if bed:
            draft.assigned_bed_id = bed.id
        if doctor:
            draft.assigned_doctor_id = doctor.id

        if bed and doctor:
            draft.status = IntakeStatus.admitted
        else:
            reasons = []
            if not bed:
                reasons.append("no_beds_available")
            if not doctor:
                reasons.append("no_doctors_available")
            draft.referral_suggestions = AssignmentService.referral_suggestions(db, reason=" & ".join(reasons))
            draft.status = IntakeStatus.referred

        db.add(draft)
        db.flush()
        return draft

    @staticmethod
    def get_draft(db: Session, draft_id: str) -> IntakeDraft:
        draft = db.get(IntakeDraft, draft_id)
        if not draft:
            raise HTTPException(status_code=404, detail="Draft not found")
        return draft

