from src.schemas import AppBaseSchema


class HealthCheckResponse(AppBaseSchema):
    """
    Health check response schema.
    """

    http: bool
    """HTTP server is running."""

    database: bool
    """Database connection is healthy."""

    git_sha: str | None = None
    """Current Git SHA of the deployed code.  Always available in remote environments,
    but would almost always be None in local development unless explicitly set.

    Helps determine if latest code is deployed and can rule out old code still being served.
    """
