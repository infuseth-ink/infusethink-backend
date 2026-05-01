"""Greetings router."""

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session

from .models import Greeting
from .schemas import GreetingPublic

router = APIRouter(prefix="/greetings", tags=["greetings"])


@router.get("", response_model=list[GreetingPublic])
def get_greetings(session: Session = Depends(get_session)):
    return session.scalars(select(Greeting)).all()
