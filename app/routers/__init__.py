from app.routers.auth import router as auth_router
from app.routers.clinical import router as clinical_router
from app.routers.emergency import router as emergency_router
from app.routers.hospital import router as hospital_router
from app.routers.intake import router as intake_router
from app.routers.patients import router as patients_router
from app.routers.realtime import router as realtime_router

__all__ = [
    "auth_router",
    "patients_router",
    "hospital_router",
    "clinical_router",
    "emergency_router",
    "intake_router",
    "realtime_router",
]

