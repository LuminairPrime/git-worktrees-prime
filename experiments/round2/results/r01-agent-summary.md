# Run r01 - agent summary

All shell and file operations ran through the audited runner `run-command.ps1 -Run r01 -Command ...`, which starts in `C:/Users/MC/Documents/git-worktrees-prime/experiments/round2/.runs/r01`. The literal path prefix `<run>` below means that run directory. The supplied guide bundled no script, so raw Git was used in every case.

## Case 01 - isolated catalog-audit checkout

Start state (read only): `case01/project` was the primary worktree on `release`, HEAD `aaa21de9350d8fc976008f7cc3170224099870e4`, working tree clean, single commit, no linked worktrees. Tracked `.gitignore` held only `review.db`.

1. Ignore coverage placed first: added the rule `.worktrees/` to the local exclude file `case01/project/.git/info/exclude`, located with `git rev-parse --path-format=absolute --git-path info/exclude`. A local exclusion was chosen over the tracked `.gitignore` so the primary checkout files stay untouched.
2. Verified before creation, from the primary, with a trailing slash: `git check-ignore -q -- ".worktrees/"` exit **0**; `git check-ignore -v` matched `.git/info/exclude:7:.worktrees/`.
3. Base resolved: `git rev-parse --verify "release^{commit}"` gave `aaa21de...`; the target path did not already exist.
4. Created: `git worktree add -b "task/catalog-audit" "<run>/case01/project/.worktrees/catalog-audit" "release"` exit 0.
5. Re-verified the ignore after creation: `git check-ignore -q -- ".worktrees/catalog-audit/"` exit **0**, matched `.git/info/exclude:7`. Primary `git status --ignored --untracked-files=all` shows `!! .worktrees/catalog-audit/`, so the new checkout is ignored and creates no untracked noise in the primary, which the repo README requires.
6. `git worktree list --porcelain` shows both entries: the primary on `refs/heads/release` at `aaa21de`, and `.worktrees/catalog-audit` on `refs/heads/task/catalog-audit` at `aaa21de`.
7. Fix applied inside the new checkout only, in `catalog.py`: `normalize_name` changed from `return value.upper()` to `return value.strip().lower()`, so it strips surrounding whitespace and returns lowercase text.
8. Project check run inside the new checkout: `python check_catalog.py` printed `check passed`, exit **0**.
9. Committed on the task branch: `7fb378c` "Fix normalize_name to strip surrounding whitespace and lowercase" (1 file changed, 1 insertion, 1 deletion). Re-ran `python check_catalog.py` after the commit: `check passed`, exit 0.

Primary left unchanged: branch `release`, HEAD still `aaa21de9350d8fc976008f7cc3170224099870e4`, clean working tree, nothing staged, no commits made on `release`.

Removed: only the regenerable `__pycache__` produced by running the check inside the task checkout, so the retained checkout is clean. Nothing else removed.

## Case 02 - repair relocated ingest worktree registration

Before state:

- `git worktree list --porcelain` from `case02/project` listed the primary (`release`, `dea5341`) plus a second entry registered at the **old** path `<run>/case02/checkouts/ingest`, branch `task/ingest`, HEAD `1a7f0dd4823daac932a2d683bbcadff852d0d8ab`, flagged `prunable gitdir file points to non-existent location`.
- The old directory did not exist; the live checkout now lives at `<run>/case02/checkouts/ingest-live`.
- Administrative record: `case02/project/.git/worktrees/ingest/gitdir` still pointed at `<run>/case02/checkouts/ingest/.git`. The relocated checkout still had a valid `.git` file pointing back to `<run>/case02/project/.git/worktrees/ingest`, so the gitdir side existed and the checkout was repairable in place.
- Working state inside the relocated checkout before repair: branch `task/ingest`, HEAD `1a7f0dd...`, one untracked file `draft-notes.txt` reading `Ingest draft notes: keep these exactly.`, SHA256 `00B46B7FF4BF9A7F994813721FA047737FD7B527EC71AC852A4383C849E5ABE7`.

Action: `git -C "<run>/case02/project" worktree repair "<run>/case02/checkouts/ingest-live"` exit **0**, printing `repair: gitdir incorrect: .../case02/project/.git/worktrees/ingest/gitdir`. The checkout was not discarded, pruned, recreated, or unlocked.

After state:

- `git worktree list --porcelain` lists the checkout at `<run>/case02/checkouts/ingest-live`, branch `refs/heads/task/ingest`, HEAD `1a7f0dd4823daac932a2d683bbcadff852d0d8ab`, **no prunable flag**.
- `git rev-parse --show-toplevel` inside the checkout returns the new location. Same branch, same commit tip.
- The `gitdir` file now reads `<run>/case02/checkouts/ingest-live/.git`.
- Uncommitted draft notes preserved: `draft-notes.txt` is still present and untracked, with the identical SHA256 `00B46B7FF4BF9A7F994813721FA047737FD7B527EC71AC852A4383C849E5ABE7`.
- `git worktree prune --dry-run --verbose` produced **no** entries, so nothing was pruned. Branch `task/ingest` tip is still `1a7f0dd`; the primary is still on `release` at `dea5341`.

Removed: nothing. Only the administrative registration path changed.

## Case 03 - isolated None-guard hotfix workspace

Primary in-progress state recorded before any action: `case03/project` on `release`, HEAD `ab4f4d153aa3c0b9fae7162630d20076e3c5ad5f`, with ` M handler.py` (uncommitted WIP normalisation rework) and untracked `knobs.yaml`. Baseline SHA256: `handler.py` = `F777A303D2900DBDFFA67B608C7334D6F8739C09A9F08DE8F951C95EA0BB40B3`, `knobs.yaml` = `DC2FEC802A8EBA0165066BB557262963AE4D7C5B8B32933A3D6170ECDC4ACB2E`.

1. Ignore coverage was already present in the tracked `.gitignore` (`/.worktrees/`). Verified before creation with a trailing slash: `git check-ignore -q -- ".worktrees/hotfix-null-guard/"` exit **0**, matched `.gitignore:1:/.worktrees/`. Re-verified after creation: exit **0**.
2. Base resolved: `git rev-parse --verify "release^{commit}"` gave `ab4f4d1...`; the target path did not exist.
3. Created: `git worktree add -b "hotfix/null-guard" "<run>/case03/project/.worktrees/hotfix-null-guard" "release"` exit 0. The new checkout held the clean committed `release` version of `handler.py` with no WIP rework, which is what kept the hotfix isolated.
4. Reproduced the incident inside the new checkout: `handle(None)` raised `TypeError: NoneType object is not subscriptable` (exit 1, expected before the fix).
5. Implemented the None guard only, in the new checkout: added `if response is None:` returning `unknown`. Nothing else changed; the uncommitted rework in the primary was not copied, and no other behaviour was touched.
6. Project check run there: `python check_handler.py` printed `check passed`, exit **0**. Extra spot check: `handle(None)` returned `unknown`, and `handle` on an email of ` A@B.C ` returned `a@b.c`.
7. Committed on the hotfix branch: `663aecd` "Guard handle(None) and map None to unknown" (`handler.py`, 2 insertions).

Primary left exactly as found: branch `release`, HEAD still `ab4f4d153aa3c0b9fae7162630d20076e3c5ad5f`, status still ` M handler.py` plus `?? knobs.yaml`, both file hashes identical to the baseline, nothing staged. No commit, copy, stash, reset, checkout, or discard was performed in the primary, and the primary was never used as the working directory for the hotfix.

Removed: only the regenerable `__pycache__` created by running the check inside the hotfix checkout. Nothing else.

## Exact paths, branches, and refs retained or removed

Retained (nothing task-owned was deleted):

- `<run>/case01/project/.worktrees/catalog-audit` on branch `task/catalog-audit`, tip `7fb378c`, not integrated into `release`. The fix is a reviewable commit only; no merge was attempted because integration was not authorised.
- `<run>/case01/project/.git/info/exclude` - added the `.worktrees/` rule.
- `<run>/case02/checkouts/ingest-live` on branch `task/ingest`, tip `1a7f0dd`, plus its untracked `draft-notes.txt`. Not deleted: it holds uncommitted work.
- `<run>/case03/project/.worktrees/hotfix-null-guard` on branch `hotfix/null-guard`, tip `663aecd`, not integrated into `release`.
- `<run>/case03/project` primary WIP: modified `handler.py` and untracked `knobs.yaml`, both untouched.
- No branch deleted, no `worktree prune` executed, no `--force` used, no unlock, no worktree or case directory recursively deleted, no remote branch operations, no publishing or merging.

## Unresolved blockers

None. All three cases were completed and verified.

## Failed commands and recovery

- `Get-ChildItem -LiteralPath (git rev-parse --git-dir)/worktrees` in case02 exited 1 with "Second path fragment must not be a drive or UNC name" from incorrect path concatenation. Recovered by re-running with an explicitly joined absolute path, which succeeded. No repository state was affected.
- The `handle(None)` reproduction in case03 exited 1 by design; that is the defect under repair, not a harness failure.
- Two runner calls used a double-quoted here-string to write this summary; PowerShell treated the markdown backticks as escapes and one was rejected by the shell safety verifier. Both failed before writing content and were replaced with single-quoted literal line arrays. No repository state was affected.

## Disclosure

Tools used: file reads for `subject-instructions.md`, `supplied-guide.md`, `TASKS.md`, and `run-command.ps1`, plus the audited runner for every shell and file operation including this summary. No skills loaded, no web or documentation research, no persistent memory tools (ICM/Engram) and no codebase-memory MCP, no inspection of controller data, no other run touched, and no modification of the outer project, tests, skills, or vendors.
