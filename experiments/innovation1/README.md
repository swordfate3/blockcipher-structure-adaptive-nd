# Innovation-One Experiment Assets

This directory is the canonical home for innovation-one experiment assets.

- `plans/`: CSV matrices consumed by `experiments/run_innovation_one_matrix.py`.
- `configs/`: JSON configs consumed by `experiments/build_plan.py`.
- `configs/remote/`: remote Windows GPU run specs consumed by the remote script generator.
- `hparam_spaces/`: JSON/YAML search spaces consumed by `experiments/run_hparam_search.py`.
- `summaries/`: hand-curated experiment summaries and comparison tables.

Legacy paths such as `experiments/plans/` and `experiments/configs/innovation1/` remain readable during the thesis cycle for old scripts and result reproduction. New experiments should prefer this directory.
