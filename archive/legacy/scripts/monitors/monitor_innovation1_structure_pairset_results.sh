#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

uv run python scripts/monitor_remote_results.py \
  --interval-minutes 30 \
  --run-id innovation1-structure-pairset-gpu0-20260605=72 \
  --run-id innovation1-structure-pairset-gpu1-20260605=36
