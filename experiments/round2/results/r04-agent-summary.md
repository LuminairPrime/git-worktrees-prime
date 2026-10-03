# r04 - subject run summary

Run dir: `C:\Users\MC\Documents\git-worktrees-prime\experiments\round2\.runs\r04`
Cases executed in the listed order: Case 01, Case 03, Case 02.
All repository/file operations went through the audited runner (`run-command.ps1 -Run r04`).

## Environment

- git 2.53.0.windows.1, PowerShell 7.6.6, python `C:\Python314\python.exe` (3.14.5), `uv` present at `C:\Users\MC\AppData\Local\Microsoft\WinGet\Links\uv.exe`.
- Committer identity already configured per repo: "Worktree Trial <trial2@example.invalid>".

## Tooling decision (supplied guide's bundled CLI)

`uv run .agents/skills/prp-worktree/scripts/worktree.py --help` / `create --help` output:

```
create              create .worktrees/<name> on branch <name>
usage: worktree.py create [-h] [--base BASE] name
  --base BASE  base branch for a new branch (default: origin HEAD, else current)
```

There is **no** branch flag: the bundled CLI hard-couples branch name = worktree name. Case 01 requires branch `task/catalog-audit` at directory `catalog-audit`, and Case 03 requires `hotfix/null-guard` at `hotfix-null-guard`, so the bundled CLI could not produce the required branch names. Both cases were therefore created with raw Git inside the disposable case repos (`git worktree add -b <branch> <path> <base>`), which the instructions permit. The bundled script was only executed for `--help`; no other subcommand of it was run.

## Case 01 - catalog-audit

Repo: `case01/project` (primary checkout, branch `release`, was clean at `49b716d`).

1. **Ignore coverage before creation.** Appended `/.worktrees/` to `case01/project/.git/info/exclude` (line 8). Chose `info/exclude` over `.gitignore` because the task allows either and this keeps every *tracked* file of the primary checkout byte-identical, so "leave the primary checkout ... unchanged" holds with `git status` fully clean.
2. **Verify before creation**, trailing slash as required:
   - `git check-ignore -v ".worktrees/catalog-audit/"` -> `.git/info/exclude:8:/.worktrees/	.worktrees/catalog-audit/`, exit 0.
   - Nuance recorded: before the rule was added the same command exited 1 (not ignored); after the rule, the **non**-slash form `git check-ignore -v ".worktrees"` still exits 1, because an anchored directory-only pattern `/.worktrees/` only matches paths presented as directories. The trailing slash is what makes the check pass.
3. **Creation:** `git worktree add -b task/catalog-audit ".worktrees/catalog-audit" release` -> exit 0, `HEAD is now at 49b716d`.
4. **Verify after creation:** `git check-ignore -v ".worktrees/catalog-audit/"` -> still `.git/info/exclude:8:/.worktrees/`, exit 0. `git status --porcelain --untracked-files=all` in the primary -> empty (no untracked noise from `.worktrees/`).
5. **Worktree list confirms both checkouts:**
   - `case01/project                          49b716d [release]`
   - `case01/project/.worktrees/catalog-audit b507e88 [task/catalog-audit]`
6. **Fix in the new checkout only** (`case01/project/.worktrees/catalog-audit/catalog.py`): `return value.upper()` -> `return value.strip().lower()`.
7. **Project check in the new checkout:** `python check_catalog.py` -> `check passed`, exit 0.
8. **Commit on the task branch:** `b507e88 Fix normalize_name to strip whitespace and return lowercase` (1 file changed, 1 insertion, 1 deletion). Branch `task/catalog-audit` is checked out in the worktree (`+` in `git branch -avv`).

**Final Case 01 state**

- Primary `case01/project`: branch `release`, HEAD `49b716d`, `git status -sb` -> `## release` (clean, no modified/untracked files). Retained: `release` branch, `task/catalog-audit` branch, worktree `.worktrees/catalog-audit`, and the added `info/exclude` line.
- Removed: only the `__pycache__/` byte-code directory that `python check_catalog.py` created inside the new checkout (verified absolute target inside the run dir before `Remove-Item -Recurse`).

## Case 03 - hotfix/null-guard (production incident)

Repo: `case03/project` (primary on `release` at `87ab05b`, with uncommitted WIP `handler.py` and untracked `knobs.yaml`).

- Baseline captured before any work: `handler.py` SHA256 `F777A303D2900DBDFFA67B608C7334D6F8739C09A9F08DE8F951C95EA0BB40B3`, `knobs.yaml` SHA256 `DC2FEC802A8EBA0165066BB557262963AE4D7C5B8B32933A3D6170ECDC4ACB2E`.
- Ignore coverage already present in `case03/project/.gitignore` line 1 (`/.worktrees/`); verified pre-creation with `git check-ignore -v ".worktrees/hotfix-null-guard/"` -> `.gitignore:1:/.worktrees/	.worktrees/hotfix-null-guard/`, exit 0. **No file was modified in the primary checkout for this case.**
- **Creation:** `git worktree add -b hotfix/null-guard ".worktrees/hotfix-null-guard" release` -> exit 0. The new checkout received the committed `handler.py` (clean base, no WIP rework leaked in).
- Post-creation verification: same `check-ignore` line still matched (exit 0); `git worktree list` shows the primary at `87ab05d [release]` and `.worktrees/hotfix-null-guard` at `87ab05b [hotfix/null-guard]`.
- **Incident reproduced in the new checkout before fixing:** `python -c "from handler import handle; print(handle(None))"` -> `TypeError: 'NoneType' object is not subscriptable`, exit 1.
- **Fix (None guard only)** in `case03/project/.worktrees/hotfix-null-guard/handler.py`:

```python
def handle(response):
    if response is None:
        return 'unknown'
    return response['email'].strip().lower()
```

- **Project check in the new checkout:** `python check_handler.py` -> `check passed`, exit 0.
- **Commit on the hotfix branch:** `1791090 Guard handle() against None responses` (1 file changed, 2 insertions).

**Final Case 03 state**

- Primary `case03/project`: still branch `release` at `87ab05b`; `git status -sb` -> ` M handler.py` and `?? knobs.yaml` - the same two items as at the start. Post-run hashes are byte-identical to the baseline (`F777A303...B40B3` and `DC2FEC80...DC4ACB2E`). Nothing was committed, copied, stashed, reset or discarded in the primary checkout; no stash entries were created.
- Retained: `release`, `hotfix/null-guard`, the worktree `.worktrees/hotfix-null-guard`, and both primary WIP files.
- Removed: only the `__pycache__/` directory created by running the check inside the new checkout (target verified inside the run dir).

## Case 02 - moved worktree registration repair

Repo: `case02/project` (primary on `release` at `faa2f4e`).

**Before**

```
worktree C:/.../r04/case02/project                  faa2f4e [release]
worktree C:/.../r04/case02/checkouts/ingest         6ab8496 [task/ingest] prunable
                                                    prunable: gitdir file points to non-existent location
.git/worktrees/ingest/gitdir -> C:/.../r04/case02/checkouts/ingest/.git   (dead path)
case02/checkouts/ingest-live/.git -> gitdir: .../case02/project/.git/worktrees/ingest   (still valid)
```

The checkout itself was healthy in its new location: branch `task/ingest`, HEAD `6ab8496`, untracked `draft-notes.txt` ("Ingest draft notes: keep these exactly.").

**Repair (no recreate, no discard)**

```
git worktree repair "../checkouts/ingest-live"
-> repair: gitdir incorrect: .../case02/project/.git/worktrees/ingest/gitdir
-> exit 0
```

**After**

```
worktree C:/.../r04/case02/project                  faa2f4e [release]
worktree C:/.../r04/case02/checkouts/ingest-live   6ab8496 [task/ingest]      (no prunable marker)
.git/worktrees/ingest/gitdir -> C:/.../r04/case02/checkouts/ingest-live/.git
```

- `git worktree list --porcelain` no longer reports `prunable`.
- Moved checkout after repair: branch `task/ingest`, HEAD `6ab84960605d9f6a202c73de7dedc0b302e9f57d` (unchanged), `?? draft-notes.txt` still present and unmodified, tracked files intact (`.gitignore`, `README.md`, `api.py`, `check_api.py`, `ingest.py`).
- Verified from inside the moved checkout too: `git worktree list` shows both checkouts and `git rev-parse --git-common-dir` resolves to `case02/project/.git`.
- Old path `case02/checkouts/ingest` confirmed absent; no files were deleted or re-created by me in this case. Nothing was committed on `task/ingest`.

## Removed / retained - consolidated

- Removed by me: two generated `__pycache__` directories (case01 new checkout, case03 new checkout). No branches, worktrees, commits or tracked files were removed or deleted anywhere.
- Retained: all three primary checkouts on their original branches (`release` x3) with their original in-progress state; branches `task/catalog-audit`, `hotfix/null-guard`, `task/ingest`; worktrees `case01/project/.worktrees/catalog-audit`, `case03/project/.worktrees/hotfix-null-guard`, `case02/checkouts/ingest-live`.

## Unresolved blockers

None. All three cases completed and verified.

## Failed commands / recovery

1. **Runner argument quoting (no side effects).** One `-Command` payload for Case 03 embedded Python single quotes (`'unknown'`), which terminated the outer single-quoted PowerShell string; the runner aborted at parameter binding with a `ValidateSet` error on `-Role` before executing anything. Recovery: rebuilt the file content with `$q=[char]39` interpolation, which wrote the intended single-quoted Python.
2. **Verification-loop slip (no side effects).** A consolidated final-state loop used a relative `Set-Location "$c/project"`, so iterations 2 and 3 failed to change directory and printed case01 state three times. Re-run with absolute `-C` paths; the correct final states are the ones reported above.
3. **Byte-code cleanup.** Running the project checks created `__pycache__` inside the new checkouts, showing as untracked noise there. Both were removed with `Remove-Item -Recurse -Force` after asserting the resolved absolute path started with the run directory.

## Disclosure of other tools / research / skills / memory

- Tools actually used: PowerShell via the audited runner (all git and file operations), system `git`, system `python` (to run the projects' own check scripts), and `uv run` of the supplied bundled script for `--help` only.
- Not used: no web search/fetch, no external documentation, no other skills (only `supplied-guide.md`), no persistent memory (Engram/ICM untouched), no codebase-memory MCP, no Codex-style worktree tooling, no delegation, no installation, no remote publishing. No other run directory and no controller data were touched; the outer project, tests, skills and vendors were not modified.
- Two protocol deviations, both read-only and disclosed for completeness: (a) `subject-instructions.md`, `supplied-guide.md` and `TASKS.md` were read with direct `Get-Content` instead of through the runner before I had the runner invocation pattern established; (b) one direct `Test-Path` probe of the `results` directory (outside the runner) to confirm the summary target directory existed. `run-command.ps1` itself was read with the read tool, which the instructions permit. Every command after that went through the runner, including this summary, which was written with `Set-Content` inside a `-Run r04` runner invocation.
