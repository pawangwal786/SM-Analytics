#!/bin/bash
set -e

echo "Setting up SM Analytics development environment..."

if [ -f "pyproject.toml" ]; then
    pip install uv
    uv sync
fi

pre-commit install || true

echo "Setup complete."
