#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../.."

WAIT_CURRICULUM='innovation1-spn-present-spnaligned-r7-curriculum-screen-gpu0-20260615=6'
WAIT_DELTA='innovation1-spn-present-delta-paligned-matrix-screen-gpu1-20260615=18'
NEXT_EVIDENCE='innovation1-spn-present-delta-paligned-tokenmixer-evidence-r7r8-gpu0-20260615'
NEXT_PLAYER='innovation1-spn-present-p-layer-mixer-r7r8-gpu1-20260615'
EVIDENCE_SCHEDULE='G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\schedule_innovation1_spn_present_delta_paligned_tokenmixer_evidence_r7r8_gpu0_20260615.cmd'
PLAYER_SCHEDULE='G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\schedule_innovation1_spn_present_p_layer_mixer_r7r8_gpu1_20260615.cmd'

while true; do
  if uv run python scripts/monitor_remote_results.py --once \
    --run-id "${WAIT_CURRICULUM}" \
    --run-id "${WAIT_DELTA}"; then
    echo "PREVIOUS_CANDIDATES_DONE launching evidence and p-layer mixer"
    ssh -o BatchMode=yes -o ConnectTimeout=8 lxy-a6000 "cmd.exe /c ${EVIDENCE_SCHEDULE}"
    ssh -o BatchMode=yes -o ConnectTimeout=8 lxy-a6000 "cmd.exe /c ${PLAYER_SCHEDULE}"
    if command -v tmux >/dev/null 2>&1; then
      tmux new-session -d -s mon_spn_evidence_r7r8 \
        "cd $(pwd) && uv run python scripts/monitor_remote_results.py --interval-minutes 5 --run-id ${NEXT_EVIDENCE}=12" || true
      tmux new-session -d -s mon_spn_player_r7r8 \
        "cd $(pwd) && uv run python scripts/monitor_remote_results.py --interval-minutes 5 --run-id ${NEXT_PLAYER}=12" || true
    fi
    exit 0
  fi
  echo "WAIT curriculum/delta result branches before launching evidence/p-layer mixer"
  sleep 1800
done
