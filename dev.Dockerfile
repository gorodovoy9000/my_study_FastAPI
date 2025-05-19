FROM python:3.12-slim

# install distro packages
RUN apt-get update -y && \
    apt-get install -y libpq-dev && \
    apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# install python UV package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# make uv project environmet global
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

# cd to app root
WORKDIR /opt/fastapi_app

# install python packages
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project
