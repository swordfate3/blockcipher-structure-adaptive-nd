#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
uv run python scripts/monitor_remote_results.py \
  --run-id innovation1-spn-present-spnaligned-r6-controls-10seed-gpu0-20260615=30
