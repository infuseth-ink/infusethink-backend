"""Greeting request/response schemas (Pydantic DTOs)."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class GreetingCreate(BaseModel):
    greeting: str
    name: str


class GreetingUpdate(BaseModel):
    greeting: str | None = None
    name: str | None = None


class GreetingPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    greeting: str
    name: str
    created_at: datetime
    updated_at: datetime


class GreetingListPublic(BaseModel):
    items: list[GreetingPublic]
    total: int
    page: int
    limit: int
