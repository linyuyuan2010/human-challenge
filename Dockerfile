FROM python:3.14-slim AS builder

WORKDIR /app

ENV UV_PYTHON_DOWNLOADS=never \
    UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

FROM python:3.14-slim

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd -m worker && mkdir -p /data && chown -R worker:worker /data /app
USER worker

COPY --from=builder --chown=worker:worker /app/.venv /app/.venv
COPY --chown=worker:worker . .
COPY .env.example /data/.env.example

VOLUME ["/data/"]
EXPOSE 8000

ENTRYPOINT ["python", "entrypoint.py"]
CMD ["gunicorn", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "human_challenge.asgi:application"]