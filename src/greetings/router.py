"""Greetings router."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session

from .models import Greeting
from .schemas import GreetingCreate, GreetingPublic, GreetingUpdate

router = APIRouter(prefix="/greetings", tags=["greetings"])


@router.get("", response_model=list[GreetingPublic])
def list_greetings(session: Session = Depends(get_session)):
    return session.scalars(select(Greeting)).all()


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
