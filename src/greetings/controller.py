"""Greetings router."""

import math
from typing import Annotated, Literal

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from wireup import Injected
from wireup.integration.fastapi import WireupRoute

from .models import Greeting
from .schemas import GreetingCreate, GreetingListPublic, GreetingPublic, GreetingUpdate


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)


class GreetingController:
    router = APIRouter(
        prefix="/greetings",
        tags=["greetings"],
        route_class=WireupRoute,
    )

    @router.get("", response_model=GreetingListPublic)
    async def list_greetings(
        self,
        session: Injected[AsyncSession],
        pagination: Annotated[PaginationParams, Query()] = PaginationParams(),
        sort: Annotated[Literal["asc", "desc"], Query()] = "asc",
    ):
        order = asc(Greeting.name) if sort == "asc" else desc(Greeting.name)
        base = select(Greeting)
        total: int = (
            await session.scalar(select(func.count()).select_from(Greeting)) or 0
        )
        offset = (pagination.page - 1) * pagination.limit
        if offset >= total > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Page {pagination.page} is out of range. "
                f"Total pages: {math.ceil(total / pagination.limit)}",
            )
        result = await session.scalars(
            base.order_by(order).offset(offset).limit(pagination.limit)
        )
        items = [GreetingPublic.model_validate(g) for g in result.all()]
        return GreetingListPublic(
            items=items, total=total, page=pagination.page, limit=pagination.limit
        )

    @router.post("", response_model=GreetingPublic, status_code=status.HTTP_201_CREATED)
    async def create_greeting(
        self, body: GreetingCreate, session: Injected[AsyncSession]
    ):
        greeting = Greeting(**body.model_dump())
        session.add(greeting)
        await session.commit()
        await session.refresh(greeting)
        return greeting

    @router.get("/{greeting_id}", response_model=GreetingPublic)
    async def get_greeting(self, greeting_id: int, session: Injected[AsyncSession]):
        greeting = await session.get(Greeting, greeting_id)
        if not greeting:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Greeting not found"
            )
        return greeting

    @router.patch("/{greeting_id}", response_model=GreetingPublic)
    async def update_greeting(
        self,
        greeting_id: int,
        body: GreetingUpdate,
        session: Injected[AsyncSession],
    ):
        greeting = await session.get(Greeting, greeting_id)
        if not greeting:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Greeting not found"
            )
        for field, value in body.model_dump(exclude_unset=True).items():
            setattr(greeting, field, value)
        await session.commit()
        await session.refresh(greeting)
        return greeting

    @router.delete("/{greeting_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_greeting(self, greeting_id: int, session: Injected[AsyncSession]):
        greeting = await session.get(Greeting, greeting_id)
        if not greeting:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Greeting not found"
            )
        await session.delete(greeting)
        await session.commit()
