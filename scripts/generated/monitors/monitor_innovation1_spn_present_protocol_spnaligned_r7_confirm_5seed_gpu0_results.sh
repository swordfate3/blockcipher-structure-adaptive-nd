#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
uv run python scripts/monitor_remote_results.py \
  --remote "${RESULT_REMOTE:-origin-ssh}" \
  --run-id innovation1-spn-present-protocol-spnaligned-r7-confirm-5seed-gpu0-20260616=10
