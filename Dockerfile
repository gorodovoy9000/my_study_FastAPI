FROM python:3.12-slim-bookworm AS base


# BUILD STAGE
FROM base AS builder
# Install distro packages
RUN apt-get update -q -y && \
    apt-get install -q -y build-essential libpq-dev && \
    apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*
# Install python UV package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set uv envs
ENV UV_PYTHON_DOWNLOADS=never \
  UV_LINK_MODE=copy \
  UV_COMPILE_BYTECODE=1 \
  UV_PROJECT_ENVIRONMENT="/app/.venv"
# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-dev --no-install-project --no-editable

# Copy project source code
COPY ./src /src
WORKDIR /src
# Install the project as dep
RUN --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-dev --no-editable


# FINAL STAGE
FROM base AS final
# Install final distro packages
RUN apt-get update -q -y && \
    apt-get install -q -y libpq5 && \
    apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*
# Set python envs
ENV PATH=/app/.venv/bin:$PATH \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1

# Copy the environment, but not the source code
COPY --from=builder /app/.venv /app/.venv
# Include alembic.ini into image for convenience
COPY ./alembic.ini /app/alembic.ini
WORKDIR /app
# Check app main module is importing
CMD ["python", "-I", "-c", "import bookings_study"]
