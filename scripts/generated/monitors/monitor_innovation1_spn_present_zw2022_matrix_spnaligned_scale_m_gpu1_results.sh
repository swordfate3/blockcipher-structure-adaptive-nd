#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
uv run python scripts/monitor_remote_results.py \
  --run-id innovation1-spn-present-zw2022-matrix-spnaligned-scale-m-gpu1-20260615=9
