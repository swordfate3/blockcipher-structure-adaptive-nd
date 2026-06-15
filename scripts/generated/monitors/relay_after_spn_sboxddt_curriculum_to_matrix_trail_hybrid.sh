#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../../.."

UPSTREAM_RUN="innovation1-spn-present-sboxddt-trailmixer-curriculum-highround-gpu0-20260615"
UPSTREAM_ROWS="4"
NEXT_RUN="innovation1-spn-present-matrix-trail-hybrid-highround-gpu0-20260615"
NEXT_ROWS="4"
SSH_TARGET="${SSH_TARGET:-lxy-a6000}"
RESULT_REMOTE="${RESULT_REMOTE:-origin-ssh}"
INTERVAL_SECONDS="${INTERVAL_SECONDS:-600}"
STATE_DIR="${STATE_DIR:-outputs/remote_results/.state}"
LAUNCHED_FLAG="${STATE_DIR}/${NEXT_RUN}.launched"
SCHEDULE_SCRIPT="G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\schedule_innovation1_spn_present_matrix_trail_hybrid_highround_gpu0_20260615.cmd"

mkdir -p "${STATE_DIR}"

while true; do
  now="$(date '+%F %T')"
  echo "[${now}] checking upstream ${UPSTREAM_RUN} before launching ${NEXT_RUN}"

  if UV_CACHE_DIR=/tmp/uv-cache PYTHONDONTWRITEBYTECODE=1 uv run python scripts/monitor_remote_results.py --remote "${RESULT_REMOTE}" --once --run-id "${NEXT_RUN}=${NEXT_ROWS}"; then
    echo "DONE ${NEXT_RUN} already retrieved"
    exit 0
  fi

  if [[ -f "${LAUNCHED_FLAG}" ]]; then
    echo "NEXT already launched; waiting for result branch"
    sleep "${INTERVAL_SECONDS}"
    continue
  fi

  if UV_CACHE_DIR=/tmp/uv-cache PYTHONDONTWRITEBYTECODE=1 uv run python scripts/monitor_remote_results.py --remote "${RESULT_REMOTE}" --once --run-id "${UPSTREAM_RUN}=${UPSTREAM_ROWS}"; then
    echo "UPSTREAM gate passed; launching ${NEXT_RUN}"
    ssh -o BatchMode=yes -o ConnectTimeout=8 "${SSH_TARGET}" "cmd.exe /c ${SCHEDULE_SCRIPT}"
    date '+%F %T' > "${LAUNCHED_FLAG}"
  else
    echo "WAIT upstream not gated yet"
  fi

  sleep "${INTERVAL_SECONDS}"
done
