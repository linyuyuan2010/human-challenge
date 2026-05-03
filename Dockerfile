FROM python:3.14-alpine AS builder

ENV UV_PYTHON_DOWNLOADS=never \
    UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple \
    UV_COMPILE_BYTECODE=0 \
    UV_LINK_MODE=copy

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev --group prod --no-editable --no-cache

FROM python:3.14-alpine

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN adduser -S -D -s /sbin/nologin worker && mkdir -p /data && chown worker /data

USER worker

COPY --from=builder --chown=worker:worker /app/.venv /app/.venv
COPY --chown=worker:worker . .

COPY .env.example /data/.env.example

VOLUME ["/data/"]
EXPOSE 8000

ENTRYPOINT ["python", "entrypoint.py"]
CMD ["gunicorn", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "human_challenge.asgi:application"]