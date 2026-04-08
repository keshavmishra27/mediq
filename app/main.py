from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import (
    auth_router,
    clinical_router,
    emergency_router,
    hospital_router,
    intake_router,
    patients_router,
    realtime_router,
)


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)

    if settings.cors_origins_list:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins_list,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(auth_router)
    app.include_router(patients_router)
    app.include_router(hospital_router)
    app.include_router(clinical_router)
    app.include_router(emergency_router)
    app.include_router(intake_router)
    app.include_router(realtime_router)

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    return app


app = create_app()

