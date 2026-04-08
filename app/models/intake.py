from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.models.enums import IntakeStatus


class IntakeDraft(Base):
    """
    Emergency intake draft.

    Created by:
    - receptionist filling a short ambulance admission form, or
    - automated calling-agent transcript parsing.
    """

    __tablename__ = "intake_drafts"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    status: Mapped[IntakeStatus] = mapped_column(Enum(IntakeStatus, name="intake_status"), index=True, default=IntakeStatus.draft)

    created_by_user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    # The "few details" captured quickly in an ambulance.
    patient_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    patient_phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    patient_age: Mapped[int | None] = mapped_column(nullable=True)
    symptoms: Mapped[str | None] = mapped_column(Text, nullable=True)
    pickup_location: Mapped[str | None] = mapped_column(Text, nullable=True)

    raw_agent_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    extracted_fields: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    # Results of automation
    assigned_bed_id: Mapped[str | None] = mapped_column(ForeignKey("beds.id", ondelete="SET NULL"), nullable=True, index=True)
    assigned_doctor_id: Mapped[str | None] = mapped_column(ForeignKey("doctor_profiles.id", ondelete="SET NULL"), nullable=True, index=True)
    referral_suggestions: Mapped[list[dict] | None] = mapped_column(JSONB, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

