FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    UV_PYTHON_DOWNLOADS=never \
    UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN useradd -m worker && mkdir -p /data && chown -R worker:worker /data /app

VOLUME ["/data/"]

USER worker

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

COPY --chown=worker:worker . .

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["entrypoint.sh"]

CMD ["sh", "-c", "gunicorn --workers $(nproc) --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 human_challenge.asgi:application"]