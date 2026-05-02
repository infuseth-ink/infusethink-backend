"""Greetings router."""

from dataclasses import dataclass
import math
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session

from src.database import get_session

from .models import Greeting
from .schemas import GreetingCreate, GreetingListPublic, GreetingPublic, GreetingUpdate

router = APIRouter(prefix="/greetings", tags=["greetings"])


@dataclass
class PaginationParams:
    page: Annotated[int, Query(ge=1)] = 1
    limit: Annotated[int, Query(ge=1, le=100)] = 20


@router.get("", response_model=GreetingListPublic)
def list_greetings(
    pagination: Annotated[PaginationParams, Depends()],
    sort: Annotated[Literal["asc", "desc"], Query()] = "asc",
    session: Session = Depends(get_session),
):
    order = asc(Greeting.name) if sort == "asc" else desc(Greeting.name)
    base = select(Greeting)
    total: int = session.scalar(select(func.count()).select_from(Greeting)) or 0
    offset = (pagination.page - 1) * pagination.limit
    if offset >= total > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Page {pagination.page} is out of range. "
            f"Total pages: {math.ceil(total / pagination.limit)}",
        )
    items = [
        GreetingPublic.model_validate(g)
        for g in session.scalars(
            base.order_by(order).offset(offset).limit(pagination.limit)
        ).all()
    ]
    return GreetingListPublic(
        items=items, total=total, page=pagination.page, limit=pagination.limit
    )


@router.post("", response_model=GreetingPublic, status_code=status.HTTP_201_CREATED)
def create_greeting(body: GreetingCreate, session: Session = Depends(get_session)):
    greeting = Greeting(**body.model_dump())
    session.add(greeting)
    session.commit()
    session.refresh(greeting)
    return greeting


@router.get("/{greeting_id}", response_model=GreetingPublic)
def get_greeting(greeting_id: int, session: Session = Depends(get_session)):
    greeting = session.get(Greeting, greeting_id)
    if not greeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Greeting not found"
        )
    return greeting


@router.patch("/{greeting_id}", response_model=GreetingPublic)
def update_greeting(
    greeting_id: int,
    body: GreetingUpdate,
    session: Session = Depends(get_session),
):
    greeting = session.get(Greeting, greeting_id)
    if not greeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Greeting not found"
        )
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(greeting, field, value)
    session.commit()
    session.refresh(greeting)
    return greeting


@router.delete("/{greeting_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_greeting(greeting_id: int, session: Session = Depends(get_session)):
    greeting = session.get(Greeting, greeting_id)
    if not greeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Greeting not found"
        )
    session.delete(greeting)
    session.commit()
