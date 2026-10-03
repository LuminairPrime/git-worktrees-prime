# Command Efficiency Telemetry — rounds 1 and 2

Source: `experiments/round{1,2}/.runs/rNN/commands.jsonl` (+ `transcript.txt`) for all 12 runs.
Conditions taken from `experiments/round{1,2}/results/verified-outcomes.json`
(`r01/r03/r05` = **ours**, `r02/r04/r06` = **prp**, identical in both rounds).

Counting rules applied so the numbers mean the same thing in both rounds:

- **cmds** = lines in `commands.jsonl`; **minutes** = last `utc` − first `utc`.
- **uv uses / repair / check-ignore / prune / force / stash** count *task-work* commands only.
  Commands whose text contains `agent-summary.md` are excluded, because agents quote the whole
  guide vocabulary inside their final report and that inflates naive substring counts badly
  (e.g. r02 round1 mentions `worktree.py` once — inside its own summary, and never runs it).
- **repair** = real `git … worktree repair` invocations; `--help`/`-h` probes counted separately.
- **force** = `--force` actually passed to `git`. **stash** = `git stash <mutation>`; `git stash list`
  is read-only and reported separately. **branch -D** counted as a literal `branch -D`.

## Round 1

| run | condition | cmds | minutes | uv uses | repair | check-ignore | force | stash | abs repair | prune | summary |
|-----|-----------|-----:|--------:|--------:|-------:|-------------:|------:|------:|-----------:|------:|:-------:|
| r01 | ours | 29 | 7.1 | 0 | 1 | 5 | 0 | 0 | **Y** | 3 | yes |
| r02 | prp  | 42 | 12.5 | 0 | 1 | 0 | 0 | 0 | **Y** | 0 | yes |
| r03 | ours | 51 | 15.1 | 0 | 1 | 3 | 0 | 0 | **Y** | 1 | yes |
| r04 | prp  | 56 | 11.2 | 6 | 1 (+1 `-h`) | 2 | 0 | 0 | **N** (relative `..\checkouts\adapter-current`) | 3 | yes |
| r05 | ours | 50 | 9.9 | 0 | 1 | 5 | 0 | 0 | **Y** | 1 | yes |
| r06 | prp  | 34 | 7.1 | 0 | 1 | 0 | 0 | 0 | **N** (no path arg, relies on cwd) | 0 | yes |

## Round 2

| run | condition | cmds | minutes | uv uses | repair | check-ignore | force | stash | abs repair | prune | summary |
|-----|-----------|-----:|--------:|--------:|-------:|-------------:|------:|------:|-----------:|------:|:-------:|
| r01 | ours | 35 | 8.6 | 0 | 1 | 4 | 0 | 0 | **Y** | 1 | yes |
| r02 | prp  | 38 | 8.7 | 3 | 1 | 5 | 0 | 0 | **Y** | 0 | yes |
| r03 | ours | 39 | 9.3 | 0 | 1 | 8 | 0 | 0 | **Y** | 3 | yes |
| r04 | prp  | 26 | 6.3 | 2 | 1 | 6 | 0 | 0 | **N** (relative `"../checkouts/ingest-live"`) | 0 | yes |
| r05 | ours | 47 | 11.0 | 0 | 1 | 5 | 0 | 0 | **Y** | 2 | yes |
| r06 | prp  | 47 | 9.4 | 4 | 1 (+1 `--help`) | 3 | 0 | 0 | **Y** | 2 | yes |

Totals: **ours** 251 cmds / 61.0 min over 6 runs (avg 41.8 cmds, 10.2 min) ·
**prp** 243 cmds / 55.2 min over 6 runs (avg 40.5 cmds, 9.2 min).

## Failure and retry accounting

| run | condition | retry (repeated cmd) | real failure (`PS>TerminatingError`) | harness noise |
|-----|-----------|---------------------:|------------------------------------:|---------------|
| r1 r04 | prp | 0 | 1 — `ReadAllBytes` on a relative path resolved against the run dir | — |
| r2 r05 | ours | 0 | 1 — same `ReadAllBytes` relative-path class | — |
| r2 r06 | prp | 0 | 1 — same `ReadAllBytes` relative-path class | — |
| r1 r02 / r1 r03 / r2 r05 | prp/ours/ours | 0 | 0 | `ParserError` while authoring the **summary file** (PowerShell quoting, not task work) |
| r2 r03 | ours | 0 | 0 | 2 Python `Traceback`s that were *deliberate* "expected to fail" pre-fix checks |

- **Zero** duplicate/retry commands in all 12 runs.
- **Zero** mutating `git stash`, **zero** real `--force`, **zero** `branch -D` anywhere in either round.
  The only `--force` string hits are the labels `"--- remove (no --force) ---"` and summary prose
  asserting the flag was *not* used; the only `stash` hits are read-only `git stash list`
  (r2 r01 ×1, r2 r05 ×2) and prose.
- The 3 genuine failures are all the same bug: reading a file by **relative** path while the
  runner's cwd was not the checkout root. 2 of 3 landed on prp runs.

## Signal highlights

1. **Neither condition saves commands or time.** ours 41.8 cmds / 10.2 min vs prp 40.5 cmds /
   9.2 min — a ~3% and ~10% gap on 6 runs each, well inside noise. Command count is *not* where
   the two guides differ.
2. **The prp CLI was largely ignored in practice.** Only 3 of 6 prp runs ever invoked
   `worktree.py` at all (r02 and r06 of round 1 never ran it once — their only `worktree.py`
   mention is inside their own summary). All 6 ours runs used `uv run` zero times.
   The prp guide says "never re-implement them with raw git", and it was re-implemented anyway.
3. **Half the CLI traffic was self-directed `--help` discovery.** Of 15 `uv run` tokens across
   the prp runs, 6 were `<subcommand> --help` probes (r1 r04 alone burned 6 tokens, 3 of them
   help). The bundled CLI advertises `--help` but the agents could not read it up front, so they
   spent ~40% of their CLI budget discovering flags. That is pure overhead the ours guide never incurs.
4. **The ours guide's one hard operational rule was obeyed 6/6: repair with an absolute path.**
   prp got 3/6 — r1 r04 and r2 r04 passed a literal relative path, and r1 r06 passed *no path at
   all*, relying on cwd. Because the prp guide never mentions repair, agents improvised. The
   absolute-path rule is the clearest, most consistent behavioural difference in the data.
5. **`check-ignore` coverage comes from the ours guide, not from diligence.** ours ran it 30 times
   across 6 runs (3–8 per run, every run); prp ran it 16 times, and two prp runs (r1 r02, r1 r06)
   ran it **zero** times. The prp guide hides checkouts via a pre-seeded `.git/info/exclude`, so
   prp agents never verify ignore coverage. This is a *guarantee* difference: ours verifies the
   destination is ignored before creating, prp trusts the scaffold.
6. **`worktree prune` shows the same trust asymmetry.** ours 11 dry-run/prune invocations,
   prp 3, with r1 r02 / r1 r06 / r2 r02 / r2 r04 never pruning at all. The ours guide's cleanup
   decision tree makes agents run `prune --dry-run` before touching stale metadata — which is
   exactly why the ours runs correctly *retained* the unmounted `offline-worker` registration
   instead of destroying it. prp has no prune concept, so it neither inspects nor risks that path.
7. **No condition caused a single data-loss event.** Zero `--force`, zero mutating stash, zero
   `branch -D`, zero retries across 494 commands. The destructive-flags concern is a property of
   the *tasks*, not of either guide; if this report is used to argue a guide is "safer", that
   argument is not supported by these runs.
8. **The "ParserError" noise is a measurement artifact, not agent behaviour.** Every `ParserError`
   in the corpus comes from agents writing their own final summary through the PowerShell runner
   (apostrophes in prose terminating an outer single-quoted `-Command`). It hits 3 of 12 runs and
   splits across both conditions. Counting it as a task failure would misattribute it; the report
   above separates it out for that reason.