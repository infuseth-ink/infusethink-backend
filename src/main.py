from fastapi import Depends, FastAPI
from sqlmodel import Session, select

from .config import get_settings
from .database import get_session
from .models import Greeting

app = FastAPI()


@app.get("/")
async def root():
    settings = get_settings()
    return {"message": "Hello World", "git_sha": settings.git_sha}


@app.get("/greetings")
def get_greetings(session: Session = Depends(get_session)):
    """Get all greetings from the database.

    Args:
        session: Database session (injected dependency)

    Returns:
        List of all greeting records
    """
    statement = select(Greeting)
    results = session.exec(statement)
    return results.all()
