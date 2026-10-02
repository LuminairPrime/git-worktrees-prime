# Behavioral trial evidence

Read the [main interpretation](../../docs/research/20-luna-behavioral-trials-summary.md) for outcomes and limits. [Verified outcomes](verified-outcomes.json) contain individual repository-state checks, original strict scores, and task scores that accept equivalent cherry-picked schema results.

Each `rNN-agent-summary.md` is the subject's own account, not the grading result. Each run's exported evidence directory contains its exact assigned tasks and guide, logged commands, transcript, and selected native Git Trace2 events (`start`, `exit`, `error`, and `def_repo`). The full raw traces and disposable repositories remain in ignored `tests/.runs/`.

`initial-state.json` preserves conditions, task order, initial commits and protected-file hashes. `preflight.json` records the fixture checks. `experiment-input-manifest.json` is the launch-time identity record; `checker-at-launch.py` preserves the original checker. `final-evidence-manifest.json` hashes the final test files and exports. Subjects received no grading key or condition map.

The controller corrected an overly strict prerequisite-ancestry criterion after launch, made Python verification suppress bytecode output, and added a supplementary `review_data_intact` indicator. Original required outcomes remain visible. `review_data_preserved` means saved outside the removed checkout; its failure does not mean data was lost if `review_data_intact` is true.
