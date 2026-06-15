#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
uv run python scripts/monitor_remote_results.py \
  --remote "${RESULT_REMOTE:-origin-ssh}" \
  --run-id innovation1-spn-present-delta-sinv-beamstats4deep3-r7-gpu1-20260616=4
