#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
uv run python scripts/monitor_remote_results.py \
  --remote "${RESULT_REMOTE:-origin-ssh}" \
  --run-id innovation1-arx-speck32-partial-inverse-r8-boundary-10seed-gpu1-20260616=20
