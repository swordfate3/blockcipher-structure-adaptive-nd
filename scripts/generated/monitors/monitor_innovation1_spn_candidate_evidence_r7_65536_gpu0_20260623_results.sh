#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
uv run python scripts/monitor_remote_results.py \
  --interval-minutes 5 \
  --run-id innovation1-spn-candidate-evidence-r7-65536-gpu0-20260623=2
