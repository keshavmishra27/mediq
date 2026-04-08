from app.schemas.auth import LoginIn, RegisterPatientIn, RegisterStaffIn, Token, UserOut
from app.schemas.clinical import (
    AppointmentCreateIn,
    AppointmentOut,
    ConsultationCreateIn,
    ConsultationOut,
    ReportCreateIn,
    ReportOut,
)
from app.schemas.common import Message
from app.schemas.emergency import EmergencyContentCreateIn, EmergencyContentOut
from app.schemas.hospital import (
    AmbulanceCreateIn,
    AmbulanceOut,
    AmbulanceUpdateIn,
    BedCreateIn,
    BedOut,
    BedUpdateIn,
    MedicineCreateIn,
    MedicineOut,
    MedicineUpdateIn,
    ReferralHospitalCreateIn,
    ReferralHospitalOut,
)
from app.schemas.intake import IntakeDraftCreateIn, IntakeDraftFromAgentTextIn, IntakeDraftOut
from app.schemas.patient import PatientProfileOut, PatientProfileUpdateIn

__all__ = [
    "Message",
    # auth
    "Token",
    "LoginIn",
    "RegisterPatientIn",
    "RegisterStaffIn",
    "UserOut",
    # patient
    "PatientProfileOut",
    "PatientProfileUpdateIn",
    # hospital
    "BedOut",
    "BedCreateIn",
    "BedUpdateIn",
    "AmbulanceOut",
    "AmbulanceCreateIn",
    "AmbulanceUpdateIn",
    "MedicineOut",
    "MedicineCreateIn",
    "MedicineUpdateIn",
    "ReferralHospitalOut",
    "ReferralHospitalCreateIn",
    # clinical
    "AppointmentCreateIn",
    "AppointmentOut",
    "ConsultationCreateIn",
    "ConsultationOut",
    "ReportCreateIn",
    "ReportOut",
    # emergency
    "EmergencyContentCreateIn",
    "EmergencyContentOut",
    # intake
    "IntakeDraftCreateIn",
    "IntakeDraftFromAgentTextIn",
    "IntakeDraftOut",
]

