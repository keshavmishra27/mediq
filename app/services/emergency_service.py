from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.emergency import EmergencyContent


class EmergencyService:
    @staticmethod
    def create_content(db: Session, *, payload: dict) -> EmergencyContent:
        c = EmergencyContent(**payload)
        db.add(c)
        db.flush()
        return c

    @staticmethod
    def list_content(db: Session, *, q: str | None = None, kind: str | None = None) -> list[EmergencyContent]:
        stmt = select(EmergencyContent)
        if kind:
            stmt = stmt.where(EmergencyContent.kind == kind)
        if q:
            stmt = stmt.where(EmergencyContent.title.ilike(f"%{q}%"))
        return db.scalars(stmt.order_by(EmergencyContent.created_at.desc())).all()

    @staticmethod
    def get_content(db: Session, content_id: str) -> EmergencyContent:
        c = db.get(EmergencyContent, content_id)
        if not c:
            raise HTTPException(status_code=404, detail="Content not found")
        return c

