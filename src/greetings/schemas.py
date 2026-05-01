"""Greeting request/response schemas (Pydantic DTOs)."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class GreetingPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    greeting: str
    name: str
    created_at: datetime
    updated_at: datetime
