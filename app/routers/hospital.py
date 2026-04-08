from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.rbac import require_roles
from app.deps import get_db
from app.models.enums import UserRole
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
from app.services.hospital_service import HospitalService

router = APIRouter(prefix="/hospital", tags=["hospital"])


# Bed management
@router.post("/beds", response_model=BedOut, dependencies=[Depends(require_roles(UserRole.receptionist, UserRole.admin))])
def create_bed(payload: BedCreateIn, db: Session = Depends(get_db)) -> BedOut:
    return HospitalService.create_bed(db, ward=payload.ward, bed_number=payload.bed_number, status=payload.status)


@router.get("/beds", response_model=list[BedOut], dependencies=[Depends(require_roles(UserRole.receptionist, UserRole.doctor, UserRole.admin))])
def list_beds(db: Session = Depends(get_db)) -> list[BedOut]:
    return HospitalService.list_beds(db)


@router.patch("/beds/{bed_id}", response_model=BedOut, dependencies=[Depends(require_roles(UserRole.receptionist, UserRole.admin))])
def update_bed(bed_id: str, payload: BedUpdateIn, db: Session = Depends(get_db)) -> BedOut:
    return HospitalService.update_bed(db, bed_id=bed_id, patch=payload.model_dump(exclude_unset=True))


# Ambulance management
@router.post("/ambulances", response_model=AmbulanceOut, dependencies=[Depends(require_roles(UserRole.receptionist, UserRole.admin))])
def create_ambulance(payload: AmbulanceCreateIn, db: Session = Depends(get_db)) -> AmbulanceOut:
    return HospitalService.create_ambulance(db, code=payload.code, status=payload.status, current_location=payload.current_location)


@router.get("/ambulances", response_model=list[AmbulanceOut], dependencies=[Depends(require_roles(UserRole.receptionist, UserRole.doctor, UserRole.admin))])
def list_ambulances(db: Session = Depends(get_db)) -> list[AmbulanceOut]:
    return HospitalService.list_ambulances(db)


@router.patch("/ambulances/{ambulance_id}", response_model=AmbulanceOut, dependencies=[Depends(require_roles(UserRole.receptionist, UserRole.admin))])
def update_ambulance(ambulance_id: str, payload: AmbulanceUpdateIn, db: Session = Depends(get_db)) -> AmbulanceOut:
    return HospitalService.update_ambulance(db, ambulance_id=ambulance_id, patch=payload.model_dump(exclude_unset=True))


# Medicine stock
@router.post("/medicines", response_model=MedicineOut, dependencies=[Depends(require_roles(UserRole.receptionist, UserRole.admin))])
def create_medicine(payload: MedicineCreateIn, db: Session = Depends(get_db)) -> MedicineOut:
    return HospitalService.create_medicine(db, payload=payload.model_dump())


@router.get("/medicines", response_model=list[MedicineOut], dependencies=[Depends(require_roles(UserRole.receptionist, UserRole.doctor, UserRole.admin))])
def list_medicines(db: Session = Depends(get_db)) -> list[MedicineOut]:
    return HospitalService.list_medicines(db)


@router.get("/medicines/alerts/low-stock", response_model=list[dict], dependencies=[Depends(require_roles(UserRole.receptionist, UserRole.admin))])
def low_stock_alerts(db: Session = Depends(get_db)) -> list[dict]:
    return HospitalService.low_stock_alerts(db)


@router.get("/medicines/alerts/expired", response_model=list[dict], dependencies=[Depends(require_roles(UserRole.receptionist, UserRole.admin))])
def expired_medicines(db: Session = Depends(get_db)) -> list[dict]:
    return HospitalService.expired_medicines(db)


@router.patch("/medicines/{medicine_id}", response_model=MedicineOut, dependencies=[Depends(require_roles(UserRole.receptionist, UserRole.admin))])
def update_medicine(medicine_id: str, payload: MedicineUpdateIn, db: Session = Depends(get_db)) -> MedicineOut:
    return HospitalService.update_medicine(db, medicine_id=medicine_id, patch=payload.model_dump(exclude_unset=True))


# Referral hospital lookup
@router.post("/referrals", response_model=ReferralHospitalOut, dependencies=[Depends(require_roles(UserRole.receptionist, UserRole.admin))])
def create_referral(payload: ReferralHospitalCreateIn, db: Session = Depends(get_db)) -> ReferralHospitalOut:
    return HospitalService.create_referral_hospital(db, payload=payload.model_dump())


@router.get("/referrals", response_model=list[ReferralHospitalOut], dependencies=[Depends(require_roles(UserRole.receptionist, UserRole.doctor, UserRole.admin))])
def list_referrals(db: Session = Depends(get_db)) -> list[ReferralHospitalOut]:
    return HospitalService.list_referral_hospitals(db)

