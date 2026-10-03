# Rounds 1-3: trials of `git-worktrees-prime` vs `prp-worktree`

Self-contained behavioral-trial experiments. Subjects were fresh agents dispatched once per run; conditions are neutral, orders rotated. Rounds reuse the historical protocol: disposable git fixtures under `.runs/`, an audited runner (`run-command.ps1`) logging commands, transcripts, and Git Trace2, and state-based outcome checks in `<round>/results/verified-outcomes.json`.

## Conditions

| Condition | Supplied guide | Extra inputs |
|---|---|---|
| `ours` | `skills/git-worktrees-prime/SKILL.md` | none |
| `prp` | `vendors/prp-worktree/SKILL.md` | `.agents/skills/prp-worktree/` copied into the run dir (bundled `scripts/worktree.py` available via `uv run`) |

## Round 1 (`experiments/round1/`)

Original Luna cases, re-run with the two new guides: isolated fix with custom destination, squash-integrated checkout cleanup with offline volume, relocated-checkout resume.

- Strict: 17/18; with the historical cherry-pick-equivalence correction: 18/18.
- r02 (prp) case03 carried the schema worker's change verbatim instead of ancestral-merge: fails strict ancestry check, passes the corrected task score (content-identical `schema.py`), consistent with the Luna trials.
- All three prp subjects reported the bundled CLI could not express the task-mandated paths and used raw git.

## Round 2 (`experiments/round2/`)

Fresh cases targeting the concepts that differentiated the third-party suite:

1. case01 nested-destination ignore gating (`info/exclude`/`.gitignore` + `check-ignore` with trailing slash, verified before and after creation, traced in the command log)
2. case02 relocated worktree registration repair (registration reconnection, absolute-path repair, branch/tip/draft preservation)
3. case03 uncommitted in-progress work must survive a hotfix-worktree isolation (no stash/reset/destructive copy)

- Strict: 17/18. Only failure: r04 (prp) case02 used `git worktree repair "../checkouts/ingest-live"` with a relative path; registration itself repaired correctly.
- r02/r06 (prp) used the bundled CLI only where the required branch name and `.worktrees/<name>` path shape matched; otherwise raw git. r02 case01 raw git for `task/catalog-audit`; r06 case01 needed `git worktree move` post-step because the CLI flattens `/` to `-` in the directory name.

## Outcome summary

| Round | Subjects | `ours` strict | `prp` strict | Notes |
|---|---|---|---|---|
| round1 | space-bunny-free | 9/9 | 8/9 (9/9 corrected) | r02 case03 ancestry equivalence |
| round2 | space-bunny-free | 9/9 | 8/9 | r04 case02 relative-path repair |
| round3 | muse-spark-1.3 | 4/6 (r05 harness-quoting incomplete) | 6/6 | edited prp script adds `--branch` + `--base` warning; all 3 prp runs used `scripts/worktree.py` create/list/remove, all 3 ours runs used raw git |

## Round 3 (`experiments/round3/`)

Two harder fixtures, Muse Spark 1.3 subjects, prp script minimally edited to be usable:

1. case01 audit checkout must derive from `main` while primary sits on legacy `dev` (one extra `legacy.txt` commit must not leak); then retire checkout via manager keeping branch.
2. case02 None-guard hotfix under dirty WIP plus a preserved colleague stash; branch/path shape fits the edited script.

- Telemetry: `script_create` true on all 3 prp runs, false on all 3 ours runs — the edit succeeded at making the script feel usable.
- r05 (ours) created both worktrees on the right bases but never committed the fixes: PowerShell quoting through the audited runner blocked Python string-literal writes, so it left both branches uncommitted. Harness artifact, not a guide decision — but it breaks the `ours` 100% streak.
- r06 (prp) initially flagged by a checker false positive (`delete-branch` mentioned inside its own summary-write command); checker now excludes summary-writing commands.

The scoring scripts remain strict-state-based; rerun `python experiments/roundN/behavioral_trials.py inspect` to regenerate.
