#!/usr/bin/env bash
set -e

echo "======================================"
echo " Running Unit Tests & Coverage        "
echo "======================================"

echo "Running pytest with coverage..."
uv run pytest tests/ --cov=core --cov-report=xml --cov-report=term

echo "✅ All tests passed."
