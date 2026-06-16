#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
uv run python scripts/monitor_remote_results.py \
  --remote "${RESULT_REMOTE:-origin-ssh}" \
  --run-id innovation1-arx-speck32-partial-inverse-paircount-p16-r7-screen-gpu1-20260616=8
