#!/usr/bin/env bash
set -euo pipefail

RUN_ID="innovation1-arx-speck32-trail-mixer-curriculum-r7r8-gpu1-20260615"
PROJECT_DIR="G:/lxy/blockcipher-structure-adaptive-nd"
SCHEDULE="G:/lxy/blockcipher-structure-adaptive-nd/scripts/generated/remote/schedule_innovation1_arx_speck32_trail_mixer_curriculum_r7r8_gpu1_20260615.cmd"
INTERVAL_SECONDS="${INTERVAL_SECONDS:-300}"
SSH_TARGET="${SSH_TARGET:-lxy-a6000}"
GPU_INDEX="${GPU_INDEX:-1}"
DRY_RUN="${DRY_RUN:-0}"

while true; do
  echo "[$(date -Is)] checking GPU${GPU_INDEX} for ${RUN_ID}"
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
  echo "[$(date -Is)] launching ${RUN_ID}"
  ssh -o BatchMode=yes -o ConnectTimeout=8 "${SSH_TARGET}" "cmd.exe /c cd /d ${PROJECT_DIR} && ${SCHEDULE}"
  echo "[$(date -Is)] launch requested"
  exit 0
done
