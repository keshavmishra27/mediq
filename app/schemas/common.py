from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class APIModel(BaseModel):
    """
    Base schema with settings that are convenient for ORM usage.
    """

    model_config = ConfigDict(from_attributes=True)


class Message(APIModel):
    message: str


class Paginated(APIModel):
    items: list[Any]
    total: int

