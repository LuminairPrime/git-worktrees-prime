# Run r02 - Subject Agent Summary

Run directory: `.runs/r02`
Cases executed in the order given by TASKS.md: **02, then 03, then 01**.
All work was done with raw Git plus the bundled `prp-worktree` CLI, entirely inside the assigned run directory, via the audited runner (`run-command.ps1 -Run r02 -Command ...`).

---

## Case 02 - Repaired worktree registration after a directory move

**Problem.** The linked checkout directory had been moved from `case02/checkouts/ingest` to `case02/checkouts/ingest-live`, but the administrative record still pointed at the old path.

### Before

```
$ git worktree list            # run from case02/project
.../case02/project               595605b [release]
.../case02/checkouts/ingest fc63a0d [task/ingest] prunable

$ git branch -vv
  release    595605b Initial API
* task/ingest fc63a0d (.../case02/checkouts/ingest) Implement streaming ingest
```

The entry was flagged `prunable` and pointed at `case02/checkouts/ingest`, which no longer existed. The stale pointer was in the admin record:

- `case02/project/.git/worktrees/ingest/gitdir` contained `.../case02/checkouts/ingest/.git` (gone)
- `case02/checkouts/ingest-live/.git` contained `gitdir: .../case02/project/.git/worktrees/ingest` (correct, still valid)
- `case02/project/.git/worktrees/ingest/HEAD` -> `ref: refs/heads/task/ingest` (correct)

The moved checkout itself was healthy:

```
$ git status --short     # from case02/checkouts/ingest-live
?? draft-notes.txt
HEAD   = fc63a0d8bb25d8b5a17bbbfcbefd55137bbcf50f
branch = task/ingest
```

### Action

Used the Git-native repair entry point, pointed at the checkout~sS~ **current** absolute path. The supplied `prp-worktree` CLI offers only `create` / `list` / `remove`, so it could not express this operation.

```
$ (Resolve-Path ..\checkouts\ingest-live).Path
C:\Users\MC\Documents\git-worktrees-prime\experiments\round2\.runs\r02\case02\checkouts\ingest-live

$ git worktree repair "C:\...\case02\checkouts\ingest-live"
repair: gitdir incorrect: C:/.../case02/project/.git/worktrees/ingest/gitdir
exit=0
```

### After

```
$ git worktree list
.../case02/project               595605b [release]
.../case02/checkouts/ingest-live fc63a0d [task/ingest]        <- `prunable` gone

$ git branch -vv
  release    595605b Initial API
* task/ingest fc63a0d (.../case02/checkouts/ingest-live) Implement streaming ingest

$ cat .git/worktrees/ingest/gitdir
C:/.../case02/checkouts/ingest-live/.git                       <- repointed
```

### Verification

| Requirement | Result |
| --- | --- |
| Git recognises the checkout at its current absolute location | Confirmed - `git worktree list` shows `case02/checkouts/ingest-live` |
| Same branch | Confirmed - `task/ingest` before and after |
| Same commit tip | Confirmed - `fc63a0d` before and after; admin `HEAD` still `ref: refs/heads/task/ingest` |
| Uncommitted draft notes preserved | Confirmed - `?? draft-notes.txt`, 40 bytes, content `Ingest draft notes: keep these exactly.` |
| Checkout not discarded or recreated | Confirmed - only the single `gitdir` file was rewritten; directory, `.git` link file, index, HEAD and reflogs untouched |
| Primary checkout unaffected | Confirmed - `case02/project` still on `release` @ `595605b`, clean working tree |

`git worktree list --porcelain` also reports both worktrees with correct `HEAD` and `branch` records and no prunable entry.

### Paths / branches

- Retained: `case02/checkouts/ingest-live` (worktree, branch `task/ingest` @ `fc63a0d`)
- Retained: `case02/project` (primary, `release` @ `595605b`)
- Removed / deleted / recreated: **nothing**

---

## Case 03 - Isolated hotfix for `handle(None)`, primary WIP left untouched

**Starting state.** Primary `case03/project` on `release` @ `c5f6d3f`, carrying in-progress rework that had to survive untouched:

```
$ git status --short
 M handler.py
?? knobs.yaml

$ cat handler.py
def handle(response):
    # WIP: normalisation rework, do not commit yet
    email = response['email'].strip().lower()
    return email
```

### Workspace creation

`.gitignore` in this repo already carried `/worktrees/`, and `git check-ignore -v .worktrees/hotfix-null-guard/` confirms it is effective.

The supplied CLI was used as the guide prescribes:

```
$ uv run ..\..\.agents\skills\prp-worktree\scripts\worktree.py create hotfix/null-guard --base release
worktree on new branch 'hotfix/null-guard' from 'release'
C:\...\case03\project\.worktrees\hotfix-null-guard
exit=0
```

Its documented naming convention (branch name = worktree name, `/` flattened to `-` in the directory) mapped the requested branch and directory exactly as the task specified.

### The fix (inside the new checkout only)

A minimal guard on the `response` argument - `None` maps to `'unknown' - and nothing else:

```python
def handle(response):
    if response is None:
        return 'unknown'
    return response['email'].strip().lower()
```

The diff was a clean 2-line insertion, with the file~sS~ original LF line endings and no BOM preserved (`core.autocrlf=false`):

```
@@ -1,2 +1,4 @@
 def handle(response):
+    if response is None:
+        return 'unknown'
     return response['email'].strip().lower()
```

### Check and commit (in the new checkout)

```
$ python check_handler.py
check passed
exit=0

$ git add handler.py
$ git commit -m "Guard handle() against None input"
[hotfix/null-guard d527609] Guard handle() against None input
 1 file changed, 2 insertions(+)
```

`python check_handler.py` writes a `__pycache__/` directory. That byproduct was confirmed to resolve inside the run directory, then removed so the hotfix worktree is left clean. It is an artifact of the check run, not part of the fix.

### Verification

| Requirement | Result |
| --- | --- |
| Worktree at `case03/project/.worktrees/hotfix-null-guard` | Confirmed |
| New branch `hotfix/null-guard` | Confirmed |
| Starting from `release` | Confirmed - parent commit `c5f6d3f` |
| None guard implemented, `None` maps to `'unknown'` | Confirmed |
| Only the None guard, no scope creep | Confirmed - nothing else touched |
| Check run inside the new checkout | Confirmed - `check passed`, exit 0 |
| Committed on the hotfix branch | Confirmed - `d527609` on `hotfix/null-guard` |
| Primary `handler.py` rework unchanged | Confirmed - still `M handler.py` with the `WIP: normalisation rework` body; my guard is **not** present there |
| Primary `knobs.yaml` untracked draft unchanged | Confirmed - still `?? knobs.yaml`, file present |
| Primary not committed / copied / stashed / reset / discarded | Confirmed - primary still on `release` @ `c5f6d3f`, HEAD unmoved, no stash taken |

Final:

```
$ git worktree list
.../case03/project                              c5f6d3f [release]
.../case03/project/.worktrees/hotfix-null-guard d527609 [hotfix/null-guard]
```

### Paths / branches

- Retained: `case03/project/.worktrees/hotfix-null-guard` (branch `hotfix/null-guard` @ `d527609`)
- Retained: `case03/project` (primary, `release` @ `c5f6d3f`, WIP intact)
- Removed: only the `__pycache__/` byproduct created by my own check run
- Removed / deleted branches: **none**

---

## Case 01 - Book-catalog audit checkout, with ignore coverage placed first

**Starting state.** Primary `case01/project` on `release` @ `3a7f620`, clean. `.gitignore` contained only `review.db` - no coverage for `.worktrees`. The repo `README.md` is explicit about the hazard:

> Catalog service. Task checkouts live under `.worktrees/<task>`. Never let a new checkout appear as untracked noise in this primary checkout.

### Step 1 - ignore coverage BEFORE creating anything

`.worktrees/` did not exist yet, so coverage was added first and proved against the not-yet-created destination.

```
$ cat .gitignore
review.db
.worktrees/

$ git check-ignore -v ".worktrees/catalog-audit/"     # trailing slash, path not yet on disk
.gitignore:2:.worktrees/	.worktrees/catalog-audit/
exit=0

$ Test-Path .worktrees
False
```

The trailing slash is load-bearing here: a directory-only pattern such as `.worktrees/` is what lets a slash-terminated path be reported as ignored, rather than falling through as untracked.

### Step 2 - create the checkout

The bundled CLI ties the branch name to the worktree name and flattens `/` to `-` in the directory, so it cannot express a `task/catalog-audit` branch living in a `catalog-audit` directory. I used the Git-native equivalent of the CLI~sS~ own `create`:

```
$ git worktree add -b task/catalog-audit .worktrees/catalog-audit release
Preparing worktree (new branch 'task/catalog-audit')
HEAD is now at 3a7f620 Initial catalog scaffold
exit=0
```

### Step 3 - post-creation verification

```
$ git worktree list
.../case01/project                            3a7f620 [release]
.../case01/project/.worktrees/catalog-audit   3a7f620 [task/catalog-audit]

$ git check-ignore -v ".worktrees/catalog-audit/"
.gitignore:2:.worktrees/	.worktrees/catalog-audit/
exit=0

$ git status --short          # primary: no untracked noise from the checkout
 M .gitignore
```

The primary shows only my intentional `.gitignore` edit - the new checkout does **not** appear as untracked noise, which is exactly what the README demands.

### Step 4 - the fix

```python
def normalize_name(value):
    return value.strip().lower()
```

```diff
 def normalize_name(value):
-    return value.upper()
+    return value.strip().lower()
```

### Step 5 - check and commit, inside the new checkout

```
$ python check_catalog.py
check passed
exit=0

$ git add catalog.py
$ git commit -m "Fix normalize_name to strip whitespace and lowercase"
[task/catalog-audit 728875d] Fix normalize_name to strip whitespace and lowercase
 1 file changed, 1 insertion(+), 1 deletion(-)
```

As in Case 03, the `__pycache__/` byproduct of the check run was verified to be inside the run directory and then removed, leaving the task branch clean.

### Verification

| Requirement | Result |
| --- | --- |
| Ignore rule added before creation | Confirmed - `.worktrees` did not exist when the rule was written and proved |
| `git check-ignore` with trailing slash, before creation | Confirmed - exit 0, matched `.gitignore:2:.worktrees/` |
| Ignore re-verified after creation | Confirmed - exit 0, same match |
| Checkout appears in `git worktree list` | Confirmed - second entry present |
| Path / branch / base | Confirmed - `.worktrees/catalog-audit` on `task/catalog-audit` from `release` @ `3a7f620` |
| `normalize_name` strips whitespace and lowercases | Confirmed - `value.strip().lower()` |
| Project check run inside the new checkout | Confirmed - `check passed`, exit 0 |
| Fix committed on the task branch | Confirmed - `728875d` on `task/catalog-audit` |
| Primary left on `release`, state unchanged | Confirmed - still `release` @ `3a7f620`, no branch switch, only the mandated `.gitignore` edit present |

### Paths / branches

- Retained: `case01/project/.worktrees/catalog-audit` (branch `task/catalog-audit` @ `728875d`)
- Retained: `case01/project` (primary, `release` @ `3a7f620`)
- Removed: only the `__pycache__/` byproduct of my own check run
- Removed / deleted branches: **none**

**Note on the `.gitignore` edit.** The task required ignore coverage in place but asked me to commit *the fix* on the task branch, and to leave the primary checkout on `release` with its state otherwise unchanged. I therefore left the `.gitignore` rule as an uncommitted modification in the primary checkout rather than committing it to `release`, which would have advanced that branch. Flagging it here so the choice is visible rather than implicit.

---

## Unresolved blockers

None. All three cases completed and verified.

## Failed commands and recovery

| Command | Outcome | Recovery |
| --- | --- | --- |
| `Set-Location ..\..\case03\project` during a combined final-verification sweep | Failed - `Cannot find path`, exit 1. Wrong number of `..` segments from `case02/checkouts/ingest-live`. | Re-ran the same verification from the run root with a single correct relative path. No state had been modified; no recovery needed. |
| First attempt to write this summary (nested single-quoted here-string passed as the runner `-Command` argument) | Failed during parameter binding, exit 1 - a quoting-parity problem in my own invocation, not a case failure. The runner never executed, so no state was touched. | Rewrote the summary using a placeholder character plus `[char]39` substitution so no literal single quote had to survive nested quoting. Wrote successfully. |

No other command failed. No destructive recovery (reset, checkout, clean, stash, prune, worktree remove) was needed anywhere.

## Exact paths / branches removed vs retained

**Removed:** nothing task-owned. Only two `__pycache__/` directories were deleted, both created by my own `check_*.py` invocations in the two worktrees I created (Case 03 `hotfix-null-guard`, Case 01 `catalog-audit`); both removal targets were resolved to absolute paths and confirmed to start with the run root before deletion.

**Branches deleted:** none. No `git worktree remove`, no `--delete-branch`, no `--force` anywhere in this run.

**Retained worktrees and branches:**

| Case | Worktree path | Branch | Tip |
| --- | --- | --- | --- |
| 01 | `case01/project` (primary) | `release` | `3a7f620` |
| 01 | `case01/project/.worktrees/catalog-audit` | `task/catalog-audit` | `728875d` |
| 02 | `case02/project` (primary) | `release` | `595605b` |
| 02 | `case02/checkouts/ingest-live` | `task/ingest` | `fc63a0d` |
| 03 | `case03/project` (primary) | `release` | `c5f6d3f` |
| 03 | `case03/project/.worktrees/hotfix-null-guard` | `hotfix/null-guard` | `d527609` |

**Commits created:** two, both on task/hotfix branches - `728875d` (Case 01) and `d527609` (Case 03). None in Case 02. No commit was created on any `release` branch.

## Tooling and disclosure

- **Shell / file operations:** exclusively via the audited runner `& <ROUND_DIR>/run-command.ps1 -Run r02 -Command <PowerShell>`. Logging was never disabled or bypassed. This includes writing this summary via `Set-Content` inside the runner, as instructed.
- **Bundled skill script used:** `.agents/skills/prp-worktree/scripts/worktree.py`, invoked exactly as the supplied guide specifies, via `uv run` - used for the Case 03 `create`. Its `--help` output was consulted to confirm available subcommands and flags. Per the guide I ran the script rather than reading its source.
- **Raw Git used for:** Case 02 `git worktree repair` (the bundled CLI has no `repair` subcommand), and Case 01 `git worktree add -b task/catalog-audit .worktrees/catalog-audit release` (the CLI name-flattening convention cannot produce a `task/catalog-audit` branch inside a `catalog-audit` directory). Both are the Git-native equivalents of the operations the guide describes.
- **Verification commands run:** `git worktree list` (plus `--porcelain`), `git branch -vv`, `git status --short`, `git rev-parse` / `--abbrev-ref HEAD`, `git check-ignore -v`, `git diff`, `git log --oneline`, `git --version`, plus `Format-Hex` for line-ending and BOM checks and `Test-Path` / `Get-Content` for file presence and content checks.
- **Python:** `python check_handler.py` (Case 03) and `python check_catalog.py` (Case 01), each run inside its new worktree. Interpreter CPython 3.14.
- **Not used:** no other skills loaded; no web search, web fetch, or documentation lookup; no persistent memory tools (ICM/Engram); no codebase-memory MCP; no Codex-style worktree tools attached to the outer project; no delegation or subagents; no reading of outer research/docs/setup scripts; no controller data; no other run directory touched; nothing in the outer project, tests, real skill, or vendors modified; no installation and no remote publishing.
