from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models.enums import AppointmentStatus, VisitType


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    patient_id: Mapped[str] = mapped_column(ForeignKey("patient_profiles.id", ondelete="CASCADE"), index=True)
    doctor_id: Mapped[str | None] = mapped_column(ForeignKey("doctor_profiles.id", ondelete="SET NULL"), index=True, nullable=True)

    scheduled_for: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    visit_type: Mapped[VisitType] = mapped_column(Enum(VisitType, name="visit_type"), index=True)
    requested_location: Mapped[str | None] = mapped_column(Text, nullable=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[AppointmentStatus] = mapped_column(
        Enum(AppointmentStatus, name="appointment_status"), index=True, default=AppointmentStatus.requested
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    patient = relationship("PatientProfile", back_populates="appointments")
    doctor = relationship("DoctorProfile", back_populates="appointments")
    consultations = relationship("Consultation", back_populates="appointment")


class Consultation(Base):
    __tablename__ = "consultations"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    appointment_id: Mapped[str | None] = mapped_column(ForeignKey("appointments.id", ondelete="SET NULL"), index=True, nullable=True)
    patient_id: Mapped[str] = mapped_column(ForeignKey("patient_profiles.id", ondelete="CASCADE"), index=True)
    doctor_id: Mapped[str] = mapped_column(ForeignKey("doctor_profiles.id", ondelete="CASCADE"), index=True)

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    vitals: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    prescriptions: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)

    appointment = relationship("Appointment", back_populates="consultations")
    patient = relationship("PatientProfile", back_populates="consultations")
    doctor = relationship("DoctorProfile", back_populates="consultations")


class ChatMessage(Base):
    """
    Stores doctor-patient chat messages for an appointment.

    WebSocket delivers messages in real-time; DB stores history for audit/continuity.
    """

    __tablename__ = "chat_messages"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    appointment_id: Mapped[str] = mapped_column(ForeignKey("appointments.id", ondelete="CASCADE"), index=True)
    sender_user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    message: Mapped[str] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    patient_id: Mapped[str] = mapped_column(ForeignKey("patient_profiles.id", ondelete="CASCADE"), index=True)
    created_by_user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[dict] = mapped_column(JSONB)  # structured report content
    pdf_url: Mapped[str | None] = mapped_column(Text, nullable=True)  # could be S3/GCS URL in prod

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)

    patient = relationship("PatientProfile", back_populates="reports")

