from fastapi import Depends, FastAPI

from .config import Settings, get_settings
from .greetings.router import router as greetings_router

app = FastAPI()
app.include_router(greetings_router)


@app.get("/")
async def root(settings: Settings = Depends(get_settings)):
    return {"message": "Hello World", "git_sha": settings.git_sha}
