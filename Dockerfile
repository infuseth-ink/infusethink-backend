FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS builder
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --frozen --no-install-project

FROM python:3.14-slim-bookworm
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini .

ARG GIT_SHA=unknown
ENV GIT_SHA=$GIT_SHA
ENV PATH="/app/.venv/bin:$PATH"

CMD ["gunicorn", "src.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
