FROM mcr.microsoft.com/devcontainers/python:3.12

RUN apt-get update && apt-get install -y \
    git \
    make \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    uv \
    pre-commit \
    ruff
