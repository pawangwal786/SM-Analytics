#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

./scripts/format.sh
./scripts/lint.sh
./scripts/test.sh

echo "Pre-commit checks passed."
