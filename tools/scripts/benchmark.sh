#!/usr/bin/env bash
set -e

echo "======================================"
echo " Running Performance Benchmarks       "
echo "======================================"

echo "Running pytest-benchmark..."
uv run pytest tests/benchmark/ --benchmark-only --benchmark-autosave

echo "✅ Benchmark Validation Passed."
