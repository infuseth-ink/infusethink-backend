from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from scalar_fastapi import get_scalar_api_reference

from .config import Settings, get_settings
from .greetings.router import router as greetings_router

app = FastAPI(docs_url=None, redoc_url=None)
app.include_router(greetings_router)


@app.get("/docs", include_in_schema=False)
async def scalar_docs() -> HTMLResponse:
    return get_scalar_api_reference(
        openapi_url="/openapi.json",
        title="Infuseth.ink API",
    )


@app.get("/")
async def root(settings: Settings = Depends(get_settings)):
    return {"message": "Hello World", "git_sha": settings.git_sha}
