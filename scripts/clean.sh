#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "Cleaning generated artifacts..."

find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true

rm -rf \
    .pytest_cache \
    .ruff_cache \
    .mypy_cache \
    .coverage \
    htmlcov \
    build \
    dist \
    .pyre \
    .pytype

echo "Clean complete."
