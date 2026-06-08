#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

uv run python scripts/monitor_remote_results.py   --interval-minutes 30   --run-id innovation1-spn-crosskey-negative-present-gpu0-20260607=48   --run-id innovation1-spn-input-ablation-present-gpu1-20260607=24
