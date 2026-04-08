from __future__ import annotations

from pydantic import Field

from app.schemas.common import APIModel


class EmergencyContentCreateIn(APIModel):
    title: str = Field(min_length=2, max_length=255)
    kind: str = Field(pattern="^(video|text|first_aid)$")
    body_text: str | None = None
    media_url: str | None = None
    tags: list[str] | None = None


class EmergencyContentOut(APIModel):
    id: str
    title: str
    kind: str
    body_text: str | None = None
    media_url: str | None = None
    tags: list[str] | None = None

