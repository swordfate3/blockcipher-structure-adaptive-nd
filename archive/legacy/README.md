# Legacy Experiment Artifacts

This folder keeps historical one-off scripts that were used to reproduce earlier innovation-one runs. They are intentionally archived outside the active `experiments/` and `scripts/` roots so new work uses generic, config-driven entry points.

## Layout

```text
archive/legacy/experiments/builders/  # old build_innovation1_* plan builders
archive/legacy/scripts/remote/        # old generated/hand-written Windows .cmd launch scripts
archive/legacy/scripts/monitors/      # old monitor_innovation1_*.sh wrappers
```

## Current Entry Points

Use these active tools for new experiments:

```bash
uv run python experiments/build_plan.py experiments/configs/innovation1/<plan>.json
uv run python scripts/generate_remote_experiment_scripts.py experiments/configs/remote/<run>.json
uv run python scripts/monitor_remote_results.py --interval-minutes 30 --run-id <run-id>=<expected-rows>
```

The archived files are kept for audit and result reproducibility only. If a historical run must be repeated exactly, use the archived script path explicitly.
