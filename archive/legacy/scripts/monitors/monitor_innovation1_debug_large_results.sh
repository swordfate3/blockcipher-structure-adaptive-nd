#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

uv run python scripts/monitor_remote_results.py \
  --interval-minutes 30 \
  --run-id innovation1-debug-large-gpu0-20260604=216 \
  --run-id innovation1-debug-large-gpu1-20260604=108
