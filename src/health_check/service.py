from wireup import injectable

from src.config import Settings

from .schemas import HealthCheckResponse


@injectable
class HealthCheckService:
    def __init__(self, settings: Settings):
        self.settings = settings

    async def check(self):
        return HealthCheckResponse(
            database=True, http=True, git_sha=self.settings.git_sha
        )
