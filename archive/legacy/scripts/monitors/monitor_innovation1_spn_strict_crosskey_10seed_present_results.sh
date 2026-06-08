#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

uv run python scripts/monitor_remote_results.py --interval-minutes 30 --run-id innovation1-spn-strict-crosskey-10seed-present-gpu0-20260608=40
