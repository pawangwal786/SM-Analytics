#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "Bootstrapping development environment..."

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

source .venv/Scripts/activate 2>/dev/null || source .venv/bin/activate

echo "Upgrading pip..."
python -m pip install --upgrade pip

echo "Installing development dependencies..."
pip install -e ".[dev,test,docs]"

echo "Bootstrap complete."
