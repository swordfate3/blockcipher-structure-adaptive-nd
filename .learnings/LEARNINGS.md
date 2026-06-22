## [LRN-20260621-001] correction

**Logged**: 2026-06-21T20:45:00+08:00
**Priority**: critical
**Status**: promoted
**Area**: docs

### Summary
Do not treat SPN/PRESENT small or medium sample runs as formal evidence that a model or route has failed.

### Details
The user corrected an important experimental interpretation error: prior SPN/PRESENT work was discussed too much like formal training, but local completed metrics show PRESENT/SPN results had only reached about `65536` samples per class. Several logs mentioning `131072` or `262144` rows were often total rows across both classes, cache/progress rows, queue plans, or incomplete runs, not completed `>100000/class` formal training.

Correct project distinction:

- Smoke/screen: below `65536/class`.
- Medium diagnostic: `65536/class` through about `524288/class`.
- Formal training: at least `1000000/class`, preferably multi-seed, fixed protocol, completed, retrieved, and plan-aligned.

For SPN/PRESENT, before claiming a route has hit its ceiling or failed, require completed and retrieved scale evidence. A `32k/class` or `65k/class` result may reject only obviously dead variants; it must not be used as a definitive conclusion that the overall route cannot improve.

Current factual baseline from the 2026-06-21 audit:

- ARX/SPECK has completed results above `100000/class`, including `131072/class` and `262144/class`.
- SPN/PRESENT completed metric rows found locally maxed out around `65536/class`.
- Therefore, prior SPN/PRESENT accuracy bottleneck claims were under-supported by large-scale evidence.

### Suggested Action
For future SPN/PRESENT experiments, always state the scale class in reports and labels. Use small runs only as screens. Before making negative claims about accuracy ceilings, run and retrieve at least a medium scale ladder such as `65536/class -> 262144/class`, and reserve "formal result" language for `>=1000000/class` multi-seed completed runs.

### Metadata
- Source: user_feedback
- Related Files: outputs/, experiments/innovation1/plans/, experiments/innovation1/configs/remote/
- Tags: spn, present, experiment-scale, formal-training, accuracy-interpretation
- Pattern-Key: innovation1.spn_present.formal_scale_required
- Recurrence-Count: 1
- First-Seen: 2026-06-21
- Last-Seen: 2026-06-21
- Promoted: AGENTS.md

---

## [LRN-20260621-003] best_practice

**Logged**: 2026-06-21T20:55:00+08:00
**Priority**: high
**Status**: promoted
**Area**: docs

### Summary
Promote only durable rules from `memory/` into `AGENTS.md`; keep experiment history and run-specific details in `memory/`.

### Details
The user approved the memory cleanup approach: do not merge all `memory/` content into `AGENTS.md`. Instead, extract compact, stable rules that affect future agent behavior. During the 2026-06-21 cleanup, repeated memory/task-plan rules were promoted for remote Windows GPU hygiene, monitor/retrieval workflow, evidence claim gates, and verification/workspace hygiene.

Specific promoted rule groups:

- Remote artifacts and generated project files must stay under `G:\lxy`.
- Windows remote schedule commands must use `cmd.exe /c`, not `cmd.exe /k`.
- After remote launch/handoff, main thread should not SSH-poll; use tmux/watchers/monitors and controlled gates.
- Result reports must distinguish planned, running, completed remotely, fallback-retrieved, verified-branch retrieved, and plan-aligned.
- Strict SPN/PRESENT claims require claim gates, encrypted-random-plaintext negatives, and explicit qualification for multi-query/application-level evidence.
- Use `uv run pytest ...`; keep project-root `tmp_*` clean.

### Suggested Action
When future memory files grow, periodically scan for repeated durable rules and promote only those concise rules to `AGENTS.md`. Leave detailed run ids, timestamps, and transient experiment states in `memory/` or `progress.md`.

### Metadata
- Source: user_feedback
- Related Files: memory/, task_plan.md, progress.md, AGENTS.md
- Tags: memory, agents, remote-workflow, evidence-gates, workspace-hygiene
- See Also: LRN-20260621-002
- Pattern-Key: workflow.memory_to_agents.promote_only_durable_rules
- Recurrence-Count: 1
- First-Seen: 2026-06-21
- Last-Seen: 2026-06-21
- Promoted: AGENTS.md

---

## [LRN-20260621-002] best_practice

**Logged**: 2026-06-21T20:43:13+08:00
**Priority**: high
**Status**: promoted
**Area**: docs

### Summary
When reading old conversation, handoff, progress, or memory documents, persist important corrections with the self-improvement workflow.

### Details
The user clarified that previous memory-document reading should use the `self-improvement` skill to store durable memory. Important findings from old dialogue, `memory/`, handoff summaries, `progress.md`, or result audits must not remain only in transient model context. If a finding changes future experimental interpretation, remote workflow, reporting language, or agent behavior, log it to `.learnings/LEARNINGS.md` using the skill format and promote concise operational rules to `AGENTS.md` when broadly applicable.

This is especially important for long-running Innovation 1 work because context-window loss and thread restarts have already caused confusion about what had actually completed, what scale counts as formal, and whether remote results were retrieved.

### Suggested Action
Before and after reading historical memory files for a major task, check whether any conclusion should be persisted. Use `.learnings/LEARNINGS.md` for detailed context and `AGENTS.md` for short rules that future agents should obey immediately.

### Metadata
- Source: user_feedback
- Related Files: memory/, progress.md, task_plan.md, .learnings/LEARNINGS.md, AGENTS.md
- Tags: memory, handoff, self-improvement, context-window, project-rules
- See Also: LRN-20260621-001
- Pattern-Key: workflow.memory_reading.persist_with_self_improvement
- Recurrence-Count: 1
- First-Seen: 2026-06-21
- Last-Seen: 2026-06-21
- Promoted: AGENTS.md

---

## [LRN-20260622-001] correction

**Logged**: 2026-06-22T11:40:00+08:00
**Priority**: critical
**Status**: promoted
**Area**: infra

### Summary
After every completed code/config/script change, make a scoped git commit and push so the workspace does not accumulate dirty state.

### Details
The user corrected a workflow failure: remote experiments are intended to pull code from GitHub, but the workspace had accumulated many uncommitted changes. To avoid committing unrelated dirty files, a remote run was started with `scp` overlays into `G:\lxy`, which made the run less reproducible than a clean GitHub commit-based launch.

Correct workflow:

- Complete code/config/script edits.
- Run appropriate verification.
- Commit only the scoped files for the completed task.
- Push the branch to the remote repository.
- Keep the workspace clean for agent-authored changes before starting new work or launching remote experiments.
- Remote experiments should default to a GitHub-pushed commit. Dirty/scp overlay launches are emergency-only and must be explicitly labeled as such in status reports and handoff notes.

This rule does not authorize reverting or committing unrelated user changes. If unrelated dirty files already exist, isolate the task's files in a scoped commit and report the remaining unrelated dirty state separately.

### Suggested Action
Promote this to `AGENTS.md` under workspace hygiene and remote workflow. Before future remote launches, run `git status --short`, ensure required files are committed and pushed, and avoid relying on scp overlays for normal experiment reproducibility.

### Metadata
- Source: user_feedback
- Related Files: AGENTS.md, .learnings/LEARNINGS.md, experiments/innovation1/configs/remote/, scripts/generated/remote/
- Tags: git, commit, push, workspace-hygiene, remote-reproducibility
- See Also: LRN-20260621-003
- Pattern-Key: workflow.git_commit_push_after_code_changes
- Recurrence-Count: 1
- First-Seen: 2026-06-22
- Last-Seen: 2026-06-22
- Promoted: AGENTS.md

---
