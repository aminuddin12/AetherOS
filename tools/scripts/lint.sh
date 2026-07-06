#!/usr/bin/env bash
set -e

echo "======================================"
echo " Running Code Quality & Linting       "
echo "======================================"

echo "1. Checking formatting with Ruff..."
uv run ruff format --check core tools tests

echo "2. Running Ruff Linter..."
uv run ruff check core tools tests

echo "3. Running Codespell..."
uv run codespell core tools tests docs

echo "4. Running Mypy..."
uv run mypy core tools tests

echo "5. Running Pyright..."
uv run pyright core tools tests

echo "✅ All code quality checks passed."
