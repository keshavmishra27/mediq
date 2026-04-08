from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.db import SessionLocal


def get_db() -> Session:
    """
    FastAPI dependency that yields a DB session per request.

    It uses a generator style so FastAPI guarantees cleanup.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

