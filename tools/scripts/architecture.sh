#!/usr/bin/env bash
set -e

echo "======================================"
echo " Running Architecture Validation      "
echo "======================================"

echo "1. Checking Import Linter Rules..."
uv run lint-imports

echo "2. Running Custom Architecture Script..."
uv run python3 tools/architecture/validate_architecture.py

echo "✅ Architecture Validation Passed."
