#!/usr/bin/env bash
set -euo pipefail

RUN_ID="innovation1-arx-speck32-trail-mixer-curriculum-r7r8-gpu1-20260615"
PROJECT_DIR="G:/lxy/blockcipher-structure-adaptive-nd"
SCHEDULE="G:/lxy/blockcipher-structure-adaptive-nd/scripts/generated/remote/schedule_innovation1_arx_speck32_trail_mixer_curriculum_r7r8_gpu1_20260615.cmd"
INTERVAL_SECONDS="${INTERVAL_SECONDS:-300}"
SSH_TARGET="${SSH_TARGET:-lxy-a6000}"

while true; do
  echo "[$(date -Is)] checking GPU1 for ${RUN_ID}"
  gpu1_processes=$(ssh -o BatchMode=yes -o ConnectTimeout=8 "${SSH_TARGET}" 'powershell -NoProfile -Command "nvidia-smi --query-compute-apps=gpu_uuid,pid,process_name,used_memory --format=csv,noheader"' || true)
  echo "${gpu1_processes}"
  if ! printf '%s\n' "${gpu1_processes}" | rg -q 'python.exe'; then
    echo "[$(date -Is)] GPU appears idle for python.exe; launching ${RUN_ID}"
    ssh -o BatchMode=yes -o ConnectTimeout=8 "${SSH_TARGET}" "cmd.exe /c cd /d ${PROJECT_DIR} && ${SCHEDULE}"
    echo "[$(date -Is)] launch requested"
    exit 0
  fi
  echo "[$(date -Is)] GPU busy; sleeping ${INTERVAL_SECONDS}s"
  sleep "${INTERVAL_SECONDS}"
done
