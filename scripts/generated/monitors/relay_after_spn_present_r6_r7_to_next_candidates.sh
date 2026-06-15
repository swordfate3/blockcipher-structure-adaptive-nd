#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../../.."

OLD_R6="innovation1-spn-present-spnaligned-r6-controls-10seed-gpu0-20260615"
OLD_R7="innovation1-spn-present-spnaligned-r7-matrix-screen-gpu1-20260615"
NEXT_CURRICULUM="innovation1-spn-present-spnaligned-r7-curriculum-screen-gpu0-20260615"
NEXT_DELTA="innovation1-spn-present-delta-paligned-matrix-screen-gpu1-20260615"

REMOTE_PROJECT='G:\lxy\blockcipher-structure-adaptive-nd'
CURRICULUM_SCHEDULE='G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\schedule_innovation1_spn_present_spnaligned_r7_curriculum_screen_gpu0_20260615.cmd'
DELTA_SCHEDULE='G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\schedule_innovation1_spn_present_delta_paligned_matrix_screen_gpu1_20260615.cmd'

while true; do
  if uv run python scripts/monitor_remote_results.py --once \
    --run-id "${OLD_R6}=30" \
    --run-id "${OLD_R7}=24"; then
    break
  fi
  echo "WAIT old r6/r7 runs not both gated yet; sleeping 600s before relay check"
  sleep 600
done

ssh -o BatchMode=yes -o ConnectTimeout=8 lxy-a6000 \
  "powershell -NoProfile -Command \"Set-Location -LiteralPath '${REMOTE_PROJECT}'; git fetch origin refactor/model-project-structure; git checkout refactor/model-project-structure; git merge --ff-only FETCH_HEAD; git rev-parse HEAD\""

ssh -o BatchMode=yes -o ConnectTimeout=8 lxy-a6000 "cmd.exe /c ${CURRICULUM_SCHEDULE}"
ssh -o BatchMode=yes -o ConnectTimeout=8 lxy-a6000 "cmd.exe /c ${DELTA_SCHEDULE}"

if ! tmux has-session -t mon_spn_r7_curriculum 2>/dev/null; then
  tmux new-session -d -s mon_spn_r7_curriculum \
    "cd $(pwd) && uv run python scripts/monitor_remote_results.py --interval-minutes 5 --run-id ${NEXT_CURRICULUM}=6"
fi

if ! tmux has-session -t mon_spn_delta_paligned_gpu1 2>/dev/null; then
  tmux new-session -d -s mon_spn_delta_paligned_gpu1 \
    "cd $(pwd) && uv run python scripts/monitor_remote_results.py --interval-minutes 5 --run-id ${NEXT_DELTA}=18"
fi

echo "RELAY launched ${NEXT_CURRICULUM} and ${NEXT_DELTA}; monitors are active."
