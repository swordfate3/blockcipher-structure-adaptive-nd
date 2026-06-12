#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
uv run python scripts/monitor_remote_results.py \
  --run-id innovation1-arx-speck32-v2-scale-m-v2-arxonly-gpu1-20260612=4
