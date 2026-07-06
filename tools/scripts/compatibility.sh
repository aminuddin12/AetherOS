#!/usr/bin/env bash
set -e

echo "======================================"
echo " Running Compatibility & Schema Checks"
echo "======================================"

echo "1. Checking Public API compatibility (Signatures)..."
uv run python3 tools/compatibility/api_checker.py

echo "2. Checking Public API compatibility (AST)..."
uv run python3 tools/compatibility/public_api_checker.py

echo "3. Checking Schema compatibility..."
uv run python3 tools/compatibility/schema_checker.py

echo "4. Checking Snapshot Tests..."
uv run pytest tests/compatibility/ --snapshot-update=false

echo "✅ Compatibility Validation Passed."
