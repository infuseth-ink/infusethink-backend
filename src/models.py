"""Database models for the application."""

from datetime import datetime
from random import randint

from pydantic import BaseModel, ConfigDict
from sqlalchemy import DateTime, func
from sqlmodel import Field, SQLModel


class AppBaseModel(BaseModel):
    """
    Base class for all SQLModel models in this application.

    Workaround from: https://github.com/fastapi/sqlmodel/discussions/855
    """

    model_config = ConfigDict(use_attribute_docstrings=True)


class AppSQLModel(AppBaseModel, SQLModel):
    """Base class for SQLModel models with common configuration.

    This class inherits from both SQLModel and AppBaseModel to provide
    consistent behavior across all models, including support for attribute
    docstrings in the generated OpenAPI schema.
    """


class Greeting(AppSQLModel, table=True):
    """Greeting table with auto-managed timestamps."""

    id: int | None = Field(default=None, primary_key=True)
    """Unique identifier for the greeting."""

    greeting: str = Field(index=True)
    """The greeting message (e.g., 'Hello', 'Hi', 'Good morning')."""

    name: str = Field(index=True)
    """The name of the person being greeted."""

    created_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"server_default": func.now()},
        nullable=False,
    )
    """Timestamp when the greeting was created."""

    updated_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()},
        nullable=False,
    )
    """Timestamp when the greeting was last updated."""


foo = "low"
bar = randint(1, 100)

foo = "high" if bar >= 50 else "low"
