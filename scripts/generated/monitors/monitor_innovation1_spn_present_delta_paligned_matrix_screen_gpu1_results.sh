#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
uv run python scripts/monitor_remote_results.py \
  --run-id innovation1-spn-present-delta-paligned-matrix-screen-gpu1-20260615=18
