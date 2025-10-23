"""Database models for the application."""

from datetime import datetime

from sqlalchemy import DateTime, func
from sqlmodel import Field, SQLModel


class Greeting(SQLModel, table=True):
    """Greeting table with auto-managed timestamps."""

    id: int | None = Field(default=None, primary_key=True)
    greeting: str = Field(index=True)
    name: str = Field(index=True)
    created_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"server_default": func.now()},
        nullable=False,
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()},
        nullable=False,
    )
