"""init schema

Revision ID: 0001_init
Revises: None
Create Date: 2026-04-08
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")

    # Enums
    user_role = postgresql.ENUM("patient", "receptionist", "doctor", "admin", name="user_role")
    appointment_status = postgresql.ENUM("requested", "confirmed", "cancelled", "completed", name="appointment_status")
    visit_type = postgresql.ENUM("hospital", "home", "requested_location", name="visit_type")
    bed_status = postgresql.ENUM("available", "occupied", "maintenance", name="bed_status")
    ambulance_status = postgresql.ENUM("available", "assigned", "maintenance", name="ambulance_status")
    intake_status = postgresql.ENUM("draft", "submitted", "admitted", "referred", name="intake_status")

    user_role.create(op.get_bind(), checkfirst=True)
    appointment_status.create(op.get_bind(), checkfirst=True)
    visit_type.create(op.get_bind(), checkfirst=True)
    bed_status.create(op.get_bind(), checkfirst=True)
    ambulance_status.create(op.get_bind(), checkfirst=True)
    intake_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("role", sa.Enum(name="user_role"), nullable=False),
        sa.Column("login_id", sa.String(length=64), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=32), nullable=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.UniqueConstraint("login_id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_users_login_id", "users", ["login_id"])
    op.create_index("ix_users_email", "users", ["email"])
    op.create_index("ix_users_phone", "users", ["phone"])
    op.create_index("ix_users_role", "users", ["role"])

    op.create_table(
        "patient_profiles",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("dob", sa.Date(), nullable=True),
        sa.Column("gender", sa.String(length=32), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("emergency_contact_name", sa.String(length=255), nullable=True),
        sa.Column("emergency_contact_phone", sa.String(length=32), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index("ix_patient_profiles_user_id", "patient_profiles", ["user_id"])

    op.create_table(
        "doctor_profiles",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("specialty", sa.String(length=255), nullable=True),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("is_available", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index("ix_doctor_profiles_user_id", "doctor_profiles", ["user_id"])
    op.create_index("ix_doctor_profiles_specialty", "doctor_profiles", ["specialty"])
    op.create_index("ix_doctor_profiles_is_available", "doctor_profiles", ["is_available"])

    op.create_table(
        "beds",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("ward", sa.String(length=64), nullable=False),
        sa.Column("bed_number", sa.String(length=32), nullable=False),
        sa.Column("status", sa.Enum(name="bed_status"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_beds_ward", "beds", ["ward"])
    op.create_index("ix_beds_bed_number", "beds", ["bed_number"])
    op.create_index("ix_beds_status", "beds", ["status"])

    op.create_table(
        "ambulances",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("status", sa.Enum(name="ambulance_status"), nullable=False),
        sa.Column("current_location", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.UniqueConstraint("code"),
    )
    op.create_index("ix_ambulances_code", "ambulances", ["code"])
    op.create_index("ix_ambulances_status", "ambulances", ["status"])

    op.create_table(
        "medicines",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("batch_no", sa.String(length=128), nullable=True),
        sa.Column("quantity", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("expiry_date", sa.Date(), nullable=True),
        sa.Column("low_stock_threshold", sa.Integer(), nullable=False, server_default=sa.text("10")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_medicines_name", "medicines", ["name"])
    op.create_index("ix_medicines_batch_no", "medicines", ["batch_no"])

    op.create_table(
        "referral_hospitals",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("address", sa.Text(), nullable=False),
        sa.Column("phone", sa.String(length=32), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_referral_hospitals_name", "referral_hospitals", ["name"])

    op.create_table(
        "appointments",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("patient_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("patient_profiles.id", ondelete="CASCADE"), nullable=False),
        sa.Column("doctor_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("doctor_profiles.id", ondelete="SET NULL"), nullable=True),
        sa.Column("scheduled_for", sa.DateTime(timezone=True), nullable=False),
        sa.Column("visit_type", sa.Enum(name="visit_type"), nullable=False),
        sa.Column("requested_location", sa.Text(), nullable=True),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("status", sa.Enum(name="appointment_status"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_appointments_patient_id", "appointments", ["patient_id"])
    op.create_index("ix_appointments_doctor_id", "appointments", ["doctor_id"])
    op.create_index("ix_appointments_scheduled_for", "appointments", ["scheduled_for"])
    op.create_index("ix_appointments_visit_type", "appointments", ["visit_type"])
    op.create_index("ix_appointments_status", "appointments", ["status"])

    op.create_table(
        "consultations",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("appointment_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("appointments.id", ondelete="SET NULL"), nullable=True),
        sa.Column("patient_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("patient_profiles.id", ondelete="CASCADE"), nullable=False),
        sa.Column("doctor_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("doctor_profiles.id", ondelete="CASCADE"), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("vitals", postgresql.JSONB(), nullable=True),
        sa.Column("prescriptions", postgresql.JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_consultations_appointment_id", "consultations", ["appointment_id"])
    op.create_index("ix_consultations_patient_id", "consultations", ["patient_id"])
    op.create_index("ix_consultations_doctor_id", "consultations", ["doctor_id"])
    op.create_index("ix_consultations_created_at", "consultations", ["created_at"])

    op.create_table(
        "chat_messages",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("appointment_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("appointments.id", ondelete="CASCADE"), nullable=False),
        sa.Column("sender_user_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_chat_messages_appointment_id", "chat_messages", ["appointment_id"])
    op.create_index("ix_chat_messages_sender_user_id", "chat_messages", ["sender_user_id"])
    op.create_index("ix_chat_messages_created_at", "chat_messages", ["created_at"])

    op.create_table(
        "reports",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("patient_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("patient_profiles.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_by_user_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("content", postgresql.JSONB(), nullable=False),
        sa.Column("pdf_url", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_reports_patient_id", "reports", ["patient_id"])
    op.create_index("ix_reports_created_by_user_id", "reports", ["created_by_user_id"])
    op.create_index("ix_reports_created_at", "reports", ["created_at"])

    op.create_table(
        "emergency_content",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("kind", sa.String(length=32), nullable=False),
        sa.Column("body_text", sa.Text(), nullable=True),
        sa.Column("media_url", sa.Text(), nullable=True),
        sa.Column("tags", postgresql.JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_emergency_content_title", "emergency_content", ["title"])
    op.create_index("ix_emergency_content_kind", "emergency_content", ["kind"])
    op.create_index("ix_emergency_content_created_at", "emergency_content", ["created_at"])

    op.create_table(
        "intake_drafts",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("status", sa.Enum(name="intake_status"), nullable=False),
        sa.Column("created_by_user_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("patient_name", sa.String(length=255), nullable=True),
        sa.Column("patient_phone", sa.String(length=32), nullable=True),
        sa.Column("patient_age", sa.Integer(), nullable=True),
        sa.Column("symptoms", sa.Text(), nullable=True),
        sa.Column("pickup_location", sa.Text(), nullable=True),
        sa.Column("raw_agent_text", sa.Text(), nullable=True),
        sa.Column("extracted_fields", postgresql.JSONB(), nullable=True),
        sa.Column("assigned_bed_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("beds.id", ondelete="SET NULL"), nullable=True),
        sa.Column("assigned_doctor_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("doctor_profiles.id", ondelete="SET NULL"), nullable=True),
        sa.Column("referral_suggestions", postgresql.JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_intake_drafts_status", "intake_drafts", ["status"])
    op.create_index("ix_intake_drafts_created_by_user_id", "intake_drafts", ["created_by_user_id"])
    op.create_index("ix_intake_drafts_assigned_bed_id", "intake_drafts", ["assigned_bed_id"])
    op.create_index("ix_intake_drafts_assigned_doctor_id", "intake_drafts", ["assigned_doctor_id"])
    op.create_index("ix_intake_drafts_created_at", "intake_drafts", ["created_at"])


def downgrade() -> None:
    op.drop_table("intake_drafts")
    op.drop_table("emergency_content")
    op.drop_table("reports")
    op.drop_table("chat_messages")
    op.drop_table("consultations")
    op.drop_table("appointments")
    op.drop_table("referral_hospitals")
    op.drop_table("medicines")
    op.drop_table("ambulances")
    op.drop_table("beds")
    op.drop_table("doctor_profiles")
    op.drop_table("patient_profiles")
    op.drop_table("users")

    op.execute("DROP TYPE IF EXISTS intake_status;")
    op.execute("DROP TYPE IF EXISTS ambulance_status;")
    op.execute("DROP TYPE IF EXISTS bed_status;")
    op.execute("DROP TYPE IF EXISTS visit_type;")
    op.execute("DROP TYPE IF EXISTS appointment_status;")
    op.execute("DROP TYPE IF EXISTS user_role;")

