from __future__ import annotations

from datetime import date

from pydantic import Field

from app.models.enums import AmbulanceStatus, BedStatus
from app.schemas.common import APIModel


class BedOut(APIModel):
    id: str
    ward: str
    bed_number: str
    status: BedStatus


class BedCreateIn(APIModel):
    ward: str = Field(min_length=1, max_length=64)
    bed_number: str = Field(min_length=1, max_length=32)
    status: BedStatus = BedStatus.available


class BedUpdateIn(APIModel):
    ward: str | None = None
    bed_number: str | None = None
    status: BedStatus | None = None


class AmbulanceOut(APIModel):
    id: str
    code: str
    status: AmbulanceStatus
    current_location: str | None = None


class AmbulanceCreateIn(APIModel):
    code: str = Field(min_length=2, max_length=64)
    status: AmbulanceStatus = AmbulanceStatus.available
    current_location: str | None = None


class AmbulanceUpdateIn(APIModel):
    status: AmbulanceStatus | None = None
    current_location: str | None = None


class MedicineOut(APIModel):
    id: str
    name: str
    batch_no: str | None = None
    quantity: int
    expiry_date: date | None = None
    low_stock_threshold: int


class MedicineCreateIn(APIModel):
    name: str = Field(min_length=1, max_length=255)
    batch_no: str | None = Field(default=None, max_length=128)
    quantity: int = 0
    expiry_date: date | None = None
    low_stock_threshold: int = 10


class MedicineUpdateIn(APIModel):
    name: str | None = None
    batch_no: str | None = None
    quantity: int | None = None
    expiry_date: date | None = None
    low_stock_threshold: int | None = None


class ReferralHospitalOut(APIModel):
    id: str
    name: str
    address: str
    phone: str | None = None
    notes: str | None = None


class ReferralHospitalCreateIn(APIModel):
    name: str = Field(min_length=2, max_length=255)
    address: str = Field(min_length=5)
    phone: str | None = None
    notes: str | None = None

