# Build Stage
FROM python:3.12-slim-bookworm AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Change the working directory to the `app` directory
WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-editable

# Copy the project into the image
ADD . /app

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-editable

# Runtime Stage
FROM python:3.12-slim-bookworm AS deploy

# Copy the application from the builder
COPY --from=builder --chown=app:app /app /app

WORKDIR /app

# Expose the port the app runs on
EXPOSE 8000

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]