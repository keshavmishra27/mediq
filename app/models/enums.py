from __future__ import annotations

import enum


class UserRole(str, enum.Enum):
    patient = "patient"
    receptionist = "receptionist"
    doctor = "doctor"
    admin = "admin"


class AppointmentStatus(str, enum.Enum):
    requested = "requested"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"


class VisitType(str, enum.Enum):
    hospital = "hospital"
    home = "home"
    requested_location = "requested_location"


class BedStatus(str, enum.Enum):
    available = "available"
    occupied = "occupied"
    maintenance = "maintenance"


class AmbulanceStatus(str, enum.Enum):
    available = "available"
    assigned = "assigned"
    maintenance = "maintenance"


class MedicineStockStatus(str, enum.Enum):
    ok = "ok"
    low = "low"
    expired = "expired"


class IntakeStatus(str, enum.Enum):
    draft = "draft"
    submitted = "submitted"
    admitted = "admitted"
    referred = "referred"

