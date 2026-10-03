# r05 agent summary

All work was done with raw Git inside the three unmanaged, disposable case repositories under `experiments/round2/.runs/r05/`. Every shell and file operation went through `run-command.ps1 -Run r05 -Command ...`. Git version: `2.53.0.windows.1` on Windows. Cases were executed in the order listed in `TASKS.md`: 02, then 01, then 03.

---

## Case 02 - repair the relocated ingest worktree registration

### Before state (observed via `git worktree list --porcelain` in `case02/project`)

| Item | Before |
|---|---|
| Registered worktree path | `.../case02/checkouts/ingest` (directory did not exist; `Test-Path` = False) |
| Git verdict | `prunable gitdir file points to non-existent location` |
| Live checkout on disk | `.../case02/checkouts/ingest-live` |
| `.git` file inside the live checkout | `gitdir: .../project/.git/worktrees/ingest` - still valid |
| Admin `.../worktrees/ingest/gitdir` | `.../case02/checkouts/ingest/.git` - dead path |
| Admin dir contents | `HEAD, commondir, gitdir, index, ORIG_HEAD, COMMIT_EDITMSG, logs/, refs/` (no in-progress operation) |
| Branch / HEAD | `task/ingest` / `73ce935828af8b7d4585c81248b077583e8e151b` |
| Uncommitted state | `?? draft-notes.txt` only (clean tracked files, no ignored files) |
| Primary | `release` @ `6f9953d`, clean |

### Action taken

Single command, run from the surviving primary checkout:

```
git -C <case02/project> worktree repair <case02/checkouts/ingest-live>
```

It printed `repair: gitdir incorrect: .../project/.git/worktrees/ingest/gitdir` and exited `0`. That diagnostic line is the command reporting the stale file it corrected; it is normal output of a successful repair, not a failure.

No prune, no recreate, no discard, no directory move or delete was performed.

### After state

| Item | After |
|---|---|
| Registered worktree path | `.../case02/checkouts/ingest-live` |
| `prunable` marker | gone |
| Admin `worktrees/ingest/gitdir` | `.../case02/checkouts/ingest-live/.git` (rewritten by repair) |
| Live checkout `.git` file | unchanged, still `.../project/.git/worktrees/ingest` |
| Branch / HEAD | `task/ingest` / `73ce935828af8b7d4585c81248b077583e8e151b` - unchanged |
| Uncommitted draft notes | `?? draft-notes.txt`; content `Ingest draft notes: keep these exactly.` - preserved |

### Verification

- `git worktree list --porcelain` lists both worktrees, no `prunable` line.
- `git worktree prune --dry-run --verbose` lists nothing (exit 0).
- `git -C <ingest-live> fsck --no-progress` - clean, no output.
- `git -C <ingest-live> rev-parse --show-toplevel` - `.../case02/checkouts/ingest-live`.
- `git branch -vv` shows `task/ingest` checked out at the new live path.
- `draft-notes.txt` still untracked and unmodified.

Note: the admin directory is still named `worktrees/ingest` although the checkout is now `ingest-live`. Git does not require the admin directory basename to match the checkout basename, and all of the verifications above confirm the registration resolves correctly. The live checkout's registration was preserved (no prune), as the guide requires.

---

## Case 01 - isolated audit checkout + `normalize_name` fix

### Location convention and ignore coverage

`README.md` in the primary states that task checkouts live under `.worktrees/<task>` and that a new checkout must never appear as untracked noise in the primary, which matches the requested destination.

Ignore coverage was placed in `case01/project/.git/info/exclude` (located via `git rev-parse --path-format=absolute --git-path info/exclude`) by appending a comment plus the rule `.worktrees/`. The tracked `.gitignore` was deliberately **not** used: editing it would have created a tracked modification in the very primary checkout the task requires to be left unchanged. `info/exclude` is a local, untracked exclusion, so it delivered the required coverage with zero working-tree impact. Verified afterwards that `.gitignore` still contains exactly `review.db` and has no local modification.

### Ignore verification before creation

```
git -C <case01/project> check-ignore -q -- ".worktrees/catalog-audit/"
  -> exit 0   (required: 0)
git -C <case01/project> check-ignore -v -- ".worktrees/catalog-audit/"
  -> .git/info/exclude:8:.worktrees/   .worktrees/catalog-audit/
```

Pre-flight checks: destination path did not already exist; branch `task/catalog-audit` did not already exist.

### Creation

```
git -C <case01/project> worktree add -b "task/catalog-audit" \
    "<case01/project>/.worktrees/catalog-audit" "release"
```

Result: `HEAD is now at 9903e46 Initial catalog scaffold`, exit 0. The base `release` was supplied explicitly and resolved to `9903e462a92981aa4644bc93a3194b167b1ac1d8`.

### Ignore verification after creation

- `check-ignore -q -- ".worktrees/catalog-audit/"` -> exit **0** again, matched by the same rule `.git/info/exclude:8:.worktrees/`.
- `git -C <primary> status --short --ignored` -> `!! .worktrees/` - present as ignored.
- `git -C <primary> status --short --branch --untracked-files=all` -> `## release` only - **no untracked noise**, satisfying the README requirement.

### Registration check

`git worktree list --porcelain` shows both the primary (`release` @ `9903e46`) and `.../case01/project/.worktrees/catalog-audit` (`task/catalog-audit`). New checkout confirmed via `rev-parse --show-toplevel`, `--abbrev-ref HEAD`, and `rev-parse HEAD`.

### The fix

Before: `return value.upper()`  ->  After: `return value.strip().lower()`

```
 def normalize_name(value):
-    return value.upper()
+    return value.strip().lower()
```

The edit was made in-place inside the new checkout only, using a targeted single-occurrence string replacement after confirming the file was plain ASCII with no BOM and LF line endings (0 CRLF, 2 bare LF). Line endings and encoding were preserved.

### Tests run (inside the new checkout)

- `python check_catalog.py` -> `check passed`, exit **0** (before commit)
- `python check_catalog.py` -> `check passed`, exit **0** (re-run after commit)

`check_catalog.py` asserts `normalize_name(' Book ') == 'book'`, so both whitespace stripping and lowercasing are exercised.

### Commit

Staged **only** `catalog.py` (`git add -- catalog.py`); the `__pycache__/` artifact was deliberately excluded. Commit `3caee5a5b45a45cf45d392e4b76e9574108c063d` on `task/catalog-audit`: `Normalize catalog names by stripping whitespace and lowercasing` (1 file changed, 1 insertion, 1 deletion).

### Primary left unchanged

Still on `release` @ `9903e46`, `git status --short --branch -uall` -> `## release` (clean), `.gitignore` unmodified.

**Integration: not performed.** Merging and publishing were not requested, and per the guide, worktree creation alone does not authorize merging. `3caee5a` remains only on `task/catalog-audit`.

---

## Case 03 - production hotfix for `handle(None)`

### Ignore coverage

The primary's `.gitignore` already contained `/.worktrees/`, so **no edit was needed or made** to the primary. Verified before and after creation:

- Before: `check-ignore -q -- ".worktrees/hotfix-null-guard/"` -> exit **0**; verbose match `.gitignore:1:/.worktrees/`.
- After: same command -> exit **0**.

Pre-flight: destination did not exist; branch `hotfix/null-guard` did not exist.

### Baseline recorded before touching anything (to prove the WIP is untouched)

| File | SHA256 |
|---|---|
| `case03/project/handler.py` (modified, WIP) | `F777A303D2900DBDFFA67B608C7334D6F8739C09A9F08DE8F951C95EA0BB40B3` |
| `case03/project/knobs.yaml` (untracked) | `DC2FEC802A8EBA0165066BB557262963AE4D7C5B8B32933A3D6170ECDC4ACB2E` |

Primary state at start: `release` @ `a4d489bee55454bb8fb93acee762a59650504b94`, with ` M handler.py` and `?? knobs.yaml`.

### Creation

```
git -C <case03/project> worktree add -b "hotfix/null-guard" \
    "<case03/project>/.worktrees/hotfix-null-guard" "release"
```

Result: `HEAD is now at a4d489b Initial handler`, exit 0.

Critically, the new checkout received the **committed** `handler.py` (`return response['email'].strip().lower()`) and **no** `knobs.yaml`. The primary's uncommitted rework did not and does not follow the new checkout, which is correct raw-Git behaviour and exactly what the task required.

### Crash reproduced first

```
python -c "from handler import handle; handle(None)"
  -> TypeError: 'NoneType' object is not subscriptable
  -> exit 1
```

### The fix - None guard only

```
 def handle(response):
+    if response is None:
+        return 'unknown'
     return response['email'].strip().lower()
```

2 added lines, nothing else changed. The existing non-None path (`response['email'].strip().lower()`) is untouched. Applied only inside the new checkout, with encoding and line endings preserved (ASCII, no BOM, LF).

### Tests run (inside the new checkout)

- `python check_handler.py` -> `check passed`, exit **0**
- `python -c "from handler import handle; print(handle(None))"` -> `unknown`, exit **0**

`check_handler.py` asserts both `handle({'email': ' A@B.C '}) == 'a@b.c'` (unchanged behaviour still correct) and `handle(None) == 'unknown'` (the fix).

### Commit

Staged **only** `handler.py`. Commit `ce150b0177f01fb60863e307314197f13091dc72` on `hotfix/null-guard`: `Guard handle(None) to return unknown` (1 file changed, 2 insertions).

### Primary verified untouched (all re-checked after the commit)

- Branch/HEAD: `release` @ `a4d489b` - unchanged; `release` ref unmoved.
- `git status --short --branch -uall` -> `## release`, ` M handler.py`, `?? knobs.yaml` - identical to start.
- `handler.py` SHA256 matches baseline -> **True**.
- `knobs.yaml` SHA256 matches baseline -> **True**; content still `normalise: true` / `rework: in-progress`.
- `git stash list` -> 0 entries (no stashing occurred).
- `git diff --stat -- .gitignore` -> empty (primary `.gitignore` unmodified).
- `handler.py` still contains the WIP rework comment `# WIP: normalisation rework, do not commit yet`.

Nothing was committed, copied, stashed, reset, or discarded from the primary.

**Integration: not performed.** Not requested; `ce150b0` remains only on `hotfix/null-guard`.

---

## Paths and refs removed / retained

**Removed: nothing.** No `git worktree remove`, no `git branch -d` or `-D`, no `git worktree prune` (only `--dry-run`, which reported nothing in all three repos), no recursive directory deletion, no `--force`, no `reset`, no `checkout --`.

**Retained (deliberate - each holds live or unintegrated task work):**

| Case | Retained checkout | Retained branch / tip | Reason |
|---|---|---|---|
| 02 | `case02/checkouts/ingest-live` | `task/ingest` @ `73ce935` | Live checkout in active use and carries uncommitted `draft-notes.txt`; it is the repaired registration, not a disposable checkout |
| 01 | `case01/project/.worktrees/catalog-audit` | `task/catalog-audit` @ `3caee5a` | Holds the unintegrated `normalize_name` fix |
| 03 | `case03/project/.worktrees/hotfix-null-guard` | `hotfix/null-guard` @ `ce150b0` | Holds the unintegrated production hotfix |

Also retained: the local exclude rule `.worktrees/` in `case01/project/.git/info/exclude` (required ignore coverage); and the primary checkouts of all three cases on `release`.

**Leftover artifacts (intentional, disclosed):** running the project checks produced untracked `__pycache__/` directories inside the case01 and case03 new checkouts. These are reproducible build output; they were deliberately **not** committed (only the source file was staged) and **not** deleted, since neither task asked for cleanup of the retained checkouts.

Final cross-case `git worktree prune --dry-run --verbose` returned nothing for all three repositories, confirming no stale registrations remain.

## Failed commands / recovery

No command failed in a way that required recovery work. Two non-zero exits occurred, both expected and benign:

1. `git -C <case02/project> worktree repair <path>` printed the diagnostic `repair: gitdir incorrect: .../worktrees/ingest/gitdir`. It **exited 0** and the repair succeeded, as confirmed by the after-state verifications above.
2. `git rev-parse --verify --quiet hotfix/null-guard` exited **1** because the branch did not yet exist. This was a deliberate pre-flight existence check; its exit code simply propagated to the runner's exit code.

Three authored commands for writing this summary also failed before the file was correct. None of them touched any case repository, and none of them altered the trial state; only the results file was involved.

1. A large PowerShell double-quoted here-string was rejected with a `ParserError`. Cause: the markdown contains single quotes (code samples such as `response['email']`), which terminated the outer shell's single-quoted `-Command` argument. Recovery: abandoned the here-string and composed the report as two literal UTF-8 text fragments, read at run time with `[System.IO.File]::ReadAllText` so no quoting layer sat between the text and `Set-Content`.
2. `String.Replace(char, string)` bound to the `char, char` overload and threw `Cannot convert argument "newChar" ... String must be exactly one character long`. Cause: an unnecessary quote-escaping step whose second argument was a 2-character string. Recovery: dropped the escaping step entirely, since a run-time variable needs no escaping, and passed the raw text to `Set-Content`.
3. The first successful write produced doubled single quotes (for example `response[''email'']`) because the output of step 2's escaping step was written instead of the raw text. Detected by post-write assertions, corrected by writing the raw text; re-verified that no doubled-quote artifacts remain and that every code literal round-tripped.

None of these three attempts affected case01, case02, or case03. All Git state reported above was verified before and after this report was written.

## Unresolved blockers

None.

## Disclosure of other tools, research, skills, and memory

- Instructions used: **only** the run-local `supplied-guide.md` and `TASKS.md`.
- No skills loaded beyond the supplied guide (the supplied guide bundles no script, so no bundled helper script existed or was used).
- No web research, no documentation or Context7 lookups, no browser use.
- No persistent-memory tools (ICM/Engram) consulted or written; no codebase-memory MCP; no subagent delegation; no repomix/deepwiki.
- No controller data, no other run directories, and no outer project, test, skill, or vendor files were read or modified. The only file outside the assigned run directory that I opened was the audited runner `run-command.ps1` itself, which the protocol explicitly permits.
- Payload staging: the summary text was composed as two literal UTF-8 fragments under `C:\Users\MC\AppData\Local\Temp\opencode\`, then read with `ReadAllText` and written to the results path by `Set-Content` executed through the audited runner. Those temp fragments are outside every case repository and contained only the report text; they are scratch and carry no trial data.
- No remote operations, no network publishing, no installations.
- All Git work used raw Git inside the three disposable case repositories; no Codex-style worktree tooling attached to the outer project.
