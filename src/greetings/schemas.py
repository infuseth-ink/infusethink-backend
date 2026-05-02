"""Greeting request/response schemas (Pydantic DTOs)."""

from datetime import datetime

from pydantic import BaseModel


class GreetingPublic(BaseModel):
    id: int
    greeting: str
    name: str
    created_at: datetime
    updated_at: datetime
