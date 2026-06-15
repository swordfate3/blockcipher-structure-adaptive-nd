#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../../.."

RUN_ID="innovation1-spn-present-protocol-spnaligned-scale-m-gpu1-20260616"
EXPECTED_ROWS="${EXPECTED_ROWS:-12}"
REMOTE_PROJECT="${REMOTE_PROJECT:-G:\\lxy\\blockcipher-structure-adaptive-nd}"
PROJECT_DIR="G:/lxy/blockcipher-structure-adaptive-nd"
SCHEDULE="G:/lxy/blockcipher-structure-adaptive-nd/scripts/generated/remote/schedule_innovation1_spn_present_protocol_spnaligned_scale_m_gpu1_20260616.cmd"
INTERVAL_SECONDS="${INTERVAL_SECONDS:-300}"
SSH_TARGET="${SSH_TARGET:-lxy-a6000}"
RESULT_REMOTE="${RESULT_REMOTE:-origin-ssh}"
GPU_INDEX="${GPU_INDEX:-1}"
DRY_RUN="${DRY_RUN:-0}"
STATE_DIR="${STATE_DIR:-outputs/remote_results/.state}"
LAUNCHED_FLAG="${STATE_DIR}/${RUN_ID}.launched"

mkdir -p "${STATE_DIR}"

monitor_result_branch_once() {
  UV_CACHE_DIR=/tmp/uv-cache PYTHONDONTWRITEBYTECODE=1 uv run python scripts/monitor_remote_results.py \
    --remote "${RESULT_REMOTE}" \
    --once \
    --run-id "${RUN_ID}=${EXPECTED_ROWS}"
}

sync_remote_project() {
  ssh -o BatchMode=yes -o ConnectTimeout=8 "${SSH_TARGET}" \
    "powershell -NoProfile -Command \"Set-Location -LiteralPath '${REMOTE_PROJECT}'; git fetch origin refactor/model-project-structure; git checkout refactor/model-project-structure; git merge --ff-only FETCH_HEAD; git rev-parse --short HEAD\""
}

while true; do
  echo "[$(date -Is)] checking GPU${GPU_INDEX} for ${RUN_ID}"

  if monitor_result_branch_once; then
    echo "[$(date -Is)] DONE ${RUN_ID} already retrieved"
    exit 0
  fi

  if [[ -f "${LAUNCHED_FLAG}" ]]; then
    echo "[$(date -Is)] run already launched; waiting for result branch"
    sleep "${INTERVAL_SECONDS}"
    continue
  fi

  gpu_table=$(ssh -o BatchMode=yes -o ConnectTimeout=8 "${SSH_TARGET}" 'nvidia-smi --query-gpu=index,uuid --format=csv,noheader' | tr -d '\r' || true)
  gpu_uuid=$(printf '%s
' "${gpu_table}" | awk -F, -v idx="${GPU_INDEX}" '$1 ~ "^ *"idx" *$" {gsub(/^ +| +$/, "", $2); print $2; exit}')
  if [[ -z "${gpu_uuid}" ]]; then
    echo "[$(date -Is)] unable to resolve GPU${GPU_INDEX} UUID; sleeping ${INTERVAL_SECONDS}s"
    printf '%s
' "${gpu_table}"
    sleep "${INTERVAL_SECONDS}"
    continue
  fi

  gpu_processes=$(ssh -o BatchMode=yes -o ConnectTimeout=8 "${SSH_TARGET}" 'nvidia-smi --query-compute-apps=gpu_uuid,pid,process_name,used_memory --format=csv,noheader' | tr -d '\r' || true)
  gpu_python_processes=$(printf '%s
' "${gpu_processes}" | awk -F, -v uuid="${gpu_uuid}" '$1 == uuid && $3 ~ /python\.exe/ {print}')
  echo "GPU${GPU_INDEX}_UUID=${gpu_uuid}"
  if [[ -n "${gpu_python_processes}" ]]; then
    printf '%s
' "${gpu_python_processes}"
    echo "[$(date -Is)] GPU${GPU_INDEX} busy; sleeping ${INTERVAL_SECONDS}s"
    sleep "${INTERVAL_SECONDS}"
    continue
  fi

  echo "[$(date -Is)] GPU${GPU_INDEX} appears idle for python.exe"
  if [[ "${DRY_RUN}" == "1" ]]; then
    echo "[$(date -Is)] DRY_RUN=1; not launching ${RUN_ID}"
    exit 0
  fi
  echo "[$(date -Is)] syncing remote project before launch"
  sync_remote_project
  echo "[$(date -Is)] launching ${RUN_ID}"
  ssh -o BatchMode=yes -o ConnectTimeout=8 "${SSH_TARGET}" "cmd.exe /c cd /d ${PROJECT_DIR} && ${SCHEDULE}"
  date '+%F %T' > "${LAUNCHED_FLAG}"
  echo "[$(date -Is)] launch requested"
  sleep "${INTERVAL_SECONDS}"
done
