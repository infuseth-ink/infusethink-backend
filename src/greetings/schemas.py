"""Greeting request/response schemas (Pydantic DTOs)."""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, model_validator

# Single source of truth for field constraints shared across DTOs
GreetingField = Annotated[str, Field(min_length=1, max_length=500)]
NameField = Annotated[str, Field(min_length=1, max_length=100)]
EmojiField = Annotated[str, Field(min_length=1, max_length=10)]


class GreetingCreate(BaseModel):
    greeting: GreetingField
    name: NameField
    emoji: EmojiField | None = None


class GreetingUpdate(BaseModel):
    # Nullable PATCH pattern — ref: https://apipark.com/techblog/en/fastapi-elegant-solutions-for-none-null-handling/
    #
    # The distinction between "unset" and "null" is preserved by using
    # model_dump(exclude_unset=True) in the router — NOT exclude_none.
    #
    # For non-nullable columns (greeting, name):
    #   - omitted  → field not in dump → DB value unchanged
    #   - null     → rejected by model_validator below → 422
    #   - value    → field in dump → DB value updated
    #
    # For nullable columns (emoji):
    #   - omitted  → field not in dump → DB value unchanged
    #   - null     → field in dump as None → DB value set to NULL (clears it)
    #   - value    → field in dump → DB value updated
    greeting: GreetingField | None = None
    name: NameField | None = None
    emoji: EmojiField | None = None

    @model_validator(mode="before")
    @classmethod
    def reject_explicit_null(cls, values: dict) -> dict:
        non_nullable = {"greeting", "name"}
        null_fields = [k for k, v in values.items() if v is None and k in non_nullable]
        if null_fields:
            raise ValueError(f"Null is not allowed for: {', '.join(null_fields)}")
        return values


class GreetingPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    greeting: str
    name: str
    emoji: str | None
    created_at: datetime
    updated_at: datetime


class GreetingListPublic(BaseModel):
    items: list[GreetingPublic]
    total: int
    page: int
    limit: int
