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
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04 AS deploy

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    build-essential \
    libncursesw5-dev \
    libssl-dev \
    libsqlite3-dev \
    tk-dev \
    libgdbm-dev \
    libc6-dev \
    libbz2-dev \
    libffi-dev \
    zlib1g-dev

# Build Python 3.12.8 from source
RUN wget https://www.python.org/ftp/python/3.12.8/Python-3.12.8.tgz && \
    tar -xf Python-3.12.8.tgz && \
    cd Python-3.12.8 && \
    ./configure --enable-optimizations --prefix=/usr/local && \
    make -j $(nproc) && \
    make install

# Create the symlink
RUN ln -s /usr/local/bin/python /usr/bin/python

# Clean up
RUN rm -rf Python-3.12.8.tgz Python-3.12.8

# Copy the application from the builder
COPY --from=builder --chown=app:app /app /app

WORKDIR /app

# Expose the port the app runs on
EXPOSE 8080

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

CMD ["serve", "run", "serve_config.yaml"]