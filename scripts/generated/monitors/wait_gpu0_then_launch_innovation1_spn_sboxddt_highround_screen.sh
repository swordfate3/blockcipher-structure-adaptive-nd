#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../../.."

SSH_TARGET="${SSH_TARGET:-lxy-a6000}"
RESULT_REMOTE="${RESULT_REMOTE:-origin-ssh}"
REMOTE_PROJECT="${REMOTE_PROJECT:-G:\\lxy\\blockcipher-structure-adaptive-nd}"
RUN_ID="${RUN_ID:-innovation1-spn-present-sboxddt-highround-screen-gpu0-20260615}"
EXPECTED_ROWS="${EXPECTED_ROWS:-8}"
SCHEDULE_SCRIPT="${SCHEDULE_SCRIPT:-G:\\lxy\\blockcipher-structure-adaptive-nd\\scripts\\generated\\remote\\schedule_innovation1_spn_present_sboxddt_highround_screen_gpu0_20260615.cmd}"
INTERVAL_SECONDS="${INTERVAL_SECONDS:-600}"
STATE_DIR="${STATE_DIR:-outputs/remote_results/.state}"
LAUNCHED_FLAG="${STATE_DIR}/${RUN_ID}.launched"

mkdir -p "${STATE_DIR}"

remote_gpu0_busy() {
  ssh -o BatchMode=yes -o ConnectTimeout=8 "${SSH_TARGET}" \
    "powershell -NoProfile -Command \"\$procs = Get-CimInstance Win32_Process -Filter \\\"name='python.exe'\\\" | Where-Object { \$_.CommandLine -like '*run_innovation_one_matrix.py*' -and \$_.CommandLine -like '*--device cuda:0*' }; if (\$procs) { \$procs | Select-Object ProcessId,CommandLine | Format-List; exit 2 } else { Write-Host 'GPU0_TRAINING_IDLE'; exit 0 }\""
}

sync_remote_project() {
  ssh -o BatchMode=yes -o ConnectTimeout=8 "${SSH_TARGET}" \
    "powershell -NoProfile -Command \"Set-Location -LiteralPath '${REMOTE_PROJECT}'; git fetch origin refactor/model-project-structure; git checkout refactor/model-project-structure; git merge --ff-only FETCH_HEAD; git rev-parse --short HEAD\""
}

launch_remote_run() {
  ssh -o BatchMode=yes -o ConnectTimeout=8 "${SSH_TARGET}" \
    "cmd.exe /c ${SCHEDULE_SCRIPT}"
}

monitor_result_branch_once() {
  uv run python scripts/monitor_remote_results.py \
    --remote "${RESULT_REMOTE}" \
    --interval-minutes "$(( INTERVAL_SECONDS / 60 ))" \
    --once \
    --run-id "${RUN_ID}=${EXPECTED_ROWS}"
}

echo "waiting for remote GPU0 before launching ${RUN_ID}"
echo "ssh_target=${SSH_TARGET}"
echo "interval_seconds=${INTERVAL_SECONDS}"

while true; do
  now="$(date '+%F %T')"
  echo "[${now}] checking result branch/gpu state"

  if monitor_result_branch_once; then
    echo "DONE ${RUN_ID} already retrieved"
    exit 0
  fi

  if [[ -f "${LAUNCHED_FLAG}" ]]; then
    echo "run already launched, waiting for result branch"
    sleep "${INTERVAL_SECONDS}"
    continue
  fi

  if remote_gpu0_busy; then
    echo "GPU0 appears idle for run_innovation_one_matrix.py; syncing and launching ${RUN_ID}"
    sync_remote_project
    launch_remote_run
    date '+%F %T' > "${LAUNCHED_FLAG}"
    echo "launched ${RUN_ID}; waiting for results branch"
  else
    echo "GPU0 still has an active matrix training process; sleeping"
  fi

  sleep "${INTERVAL_SECONDS}"
done
