#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
uv run python scripts/monitor_remote_results.py \
  --remote "${RESULT_REMOTE:-origin-ssh}" \
  --fallback-remote-run-root "${FALLBACK_REMOTE_RUN_ROOT:-lxy-a6000:G:/lxy/blockcipher-structure-adaptive-nd-runs}" \
  --fallback-output-dir "${FALLBACK_OUTPUT_DIR:-outputs/remote_results_incomplete}" \
  --run-id innovation1-spn-present-stats-hybrid-beamstats8deep4-r7-gpu0-20260616=4
