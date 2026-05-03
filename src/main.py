from fastapi import Depends, FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from scalar_fastapi import get_scalar_api_reference
import wireup
import wireup.integration.fastapi

from .config import Settings, get_settings
from .greetings.router import router as greetings_router

app = FastAPI(docs_url=None, redoc_url=None)
app.include_router(greetings_router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title="Infuseth.ink API",
        version="0.1.0",
        routes=app.routes,
    )
    http_methods = {
        "get",
        "put",
        "post",
        "delete",
        "options",
        "head",
        "patch",
        "trace",
    }
    for path in schema.get("paths", {}).values():
        if not isinstance(path, dict):
            continue
        for method, operation in path.items():
            if method not in http_methods or not isinstance(operation, dict):
                continue
            for response in operation.get("responses", {}).values():
                if not isinstance(response, dict):
                    continue
                for content in response.get("content", {}).values():
                    if not isinstance(content, dict):
                        continue
                    content_schema = content.get("schema", {})
                    if content_schema.get("type") == "array":
                        content_schema.pop("title", None)
    app.openapi_schema = schema
    return schema


app.openapi = custom_openapi


@app.get("/docs", include_in_schema=False)
async def scalar_docs() -> HTMLResponse:
    return get_scalar_api_reference(
        openapi_url="/openapi.json",
        title="Infuseth.ink API",
    )


@app.get("/")
async def root(settings: Settings = Depends(get_settings)):
    return {"message": "Hello World", "git_sha": settings.git_sha}


container = wireup.create_async_container(injectables=[])
wireup.integration.fastapi.setup(container, app)
