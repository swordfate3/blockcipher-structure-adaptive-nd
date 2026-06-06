#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

uv run python scripts/monitor_remote_results.py --interval-minutes 30 --run-id innovation1-moe-v5-hpo-best-validate-present-gpu1-20260606=20
