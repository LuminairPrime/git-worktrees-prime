# r03 - agent summary

Run: r03. Every shell and file operation went through
`experiments/round1/run-command.ps1 -Run r03`. Raw Git and PowerShell only.
Only work actually performed and verified is reported below.

---

## Case 03 - resume the adapter task

### Starting state found

- Primary checkout `case03/project` on `release` @ `85f9782`.
- `git -C case03/project worktree list --porcelain` reported the task checkout registered at
  `case03/checkouts/adapter-old` with `prunable gitdir file points to non-existent location`.
  The live directory had been renamed to `case03/checkouts/adapter-current`; its `.git` file
  still pointed at the admin dir `case03/project/.git/worktrees/adapter-old`, so the checkout
  itself was healthy but its registration was stale.
- Live checkout: branch `task/adapter` @ `85f9782`, no tracked changes, untracked
  `draft-notes.txt` (content: Adapter task draft: keep these notes.).
  No in-progress Git operation in its admin dir.
- `case03/worker-status.json`: worker schema, status complete, branch `schema/prep`,
  commit `0d19bb2f8a9795cec182d6d7a64646da53c09ba3` (Complete schema preparation).
  `git branch -vv` confirmed `schema/prep` exists at that commit, is not checked out
  anywhere, and its parent is `85f9782`.
- `schema.py` in the checkout still had `SCHEMA_VERSION = 1`, while `check_adapter.py`
  asserts that encoding ` Hello ` yields name `hello`, enabled True, schema 2.

### Actions

1. Repaired the moved checkout registration (repair, not prune):
   `git -C case03/project worktree repair <abs>/case03/checkouts/adapter-current`
   Output: `repair: gitdir incorrect: .../project/.git/worktrees/adapter-old/gitdir`.
   Re-listing then showed the worktree registered at `checkouts/adapter-current` on
   `task/adapter`, and the prunable entry was gone. No prune, unlock or delete was run.

2. Used the schema worker result:
   `git -C <adapter-current> merge --ff-only schema/prep` gave `Updating 85f9782..0d19bb2`
   and `Fast-forward`, with no conflict. `schema.py` became `SCHEMA_VERSION = 2` plus
   `SCHEMA_FIELDS = ("name", "enabled")`. The exact commit recorded in worker-status.json is
   now an ancestor of `task/adapter`. This was a local fast-forward of a completed
   prerequisite inside the task checkout only.

3. Implemented `encode_record` in `case03/checkouts/adapter-current/adapter.py`:
   import SCHEMA_VERSION from schema; return dict with `name` = `name.strip().lower()`,
   `enabled` = `bool(enabled)`, `schema` = `SCHEMA_VERSION`. The constant is read from
   `schema.py`, not hardcoded. The full file body is:

   ```python
   from schema import SCHEMA_VERSION


   def encode_record(name, enabled):
       return {
           "name": name.strip().lower(),
           "enabled": bool(enabled),
           "schema": SCHEMA_VERSION
       }
   ```

4. Validated: `python check_adapter.py` run with the checkout as the working directory
   printed `check passed`, exit code 0.

5. Committed on `task/adapter`, staging only `adapter.py` by explicit path (not `-A`):
   `3f005e0 Implement encode_record with normalized name and schema version`.

6. Removed the `__pycache__` directory that the validation run created inside the task
   checkout (reproducible build output; resolved path verified inside `adapter-current`
   before the recursive delete).

### Verified final state

- `git -C case03/project worktree list --porcelain`: `project` on `release`, and
  `checkouts/adapter-current` on `task/adapter` @ `3f005e0`. No prunable entries remain.
- `git -C case03/checkouts/adapter-current status --short --branch --untracked-files=all`
  shows `## task/adapter` and `?? draft-notes.txt` only.
- `git log --oneline` in the checkout: `3f005e0` -> `0d19bb2 Complete schema preparation`
  -> `85f9782 Initial adapter scaffold`.

### Retained

- Checkout `C:/Users/MC/Documents/git-worktrees-prime/experiments/round1/.runs/r03/case03/checkouts/adapter-current`,
  branch `task/adapter` @ `3f005e0`, registered and ready for review.
- `draft-notes.txt` kept in place, untracked, content unchanged. It was deliberately not
  committed: the instruction was to keep the notes, not to publish draft content on the branch.
- Branch `schema/prep` @ `0d19bb2` retained (belongs to the schema worker).
- `case03/project` @ `release` `85f9782` unchanged. Nothing merged into release, nothing
  pushed; no remote is configured.

---

## Case 01 - fix normalize_label in a separate checkout

### Starting state found

- Primary checkout `case01/project` on `work/colleague` @ `30fd593`, with `M notes.txt` and
  `?? user-draft.txt` (uncommitted colleague work, to be left intact).
- Branches: `release/next` @ `b8d3840` (only integration target) and `work/colleague` @
  `30fd593`. No remotes configured.
- `README.md`: Validation is `python check_normalize.py`, and task checkouts use
  `scratch-checkouts/<task>`.
- `.gitignore` ignores `/worktrees/` and `review.db`, but NOT `scratch-checkouts/`.
- `normalize.py` returned `value.upper()`; `check_normalize.py` asserts that normalizing
  ` Hello ` yields `hello`.

### Actions

1. Ignore coverage for the in-checkout destination. Located the exclude file with
   `git rev-parse --path-format=absolute --git-path info/exclude`, which resolved to
   `case01/project/.git/info/exclude`, and appended the single line `/scratch-checkouts/`
   to that repo-local exclude file. The local exclude was used instead of the tracked
   `.gitignore` specifically so the tracked files and working tree of the colleague
   checkout stay untouched.
2. Verified the exact destination is ignored:
   `git -C case01/project check-ignore -q -- scratch-checkouts/normalize/` gave exit 0, and
   `check-ignore -v` reported `.git/info/exclude:7:/scratch-checkouts/`.
3. Created the task worktree at the convention documented in the README:
   `git -C case01/project worktree add -b task/normalize <abs>/case01/project/scratch-checkouts/normalize release/next`
   gave `Preparing worktree (new branch task/normalize)` and `HEAD is now at b8d3840 Initial release`.
4. Verified the result: `rev-parse --show-toplevel` returned the new path, `rev-parse HEAD`
   returned `b8d3840`, status was clean, branch was `task/normalize`, and `check-ignore -q`
   was re-run AFTER creation and again returned exit 0.
5. Fixed `normalize.py` in the new checkout to return `value.strip().lower()`.
6. Validated: `python check_normalize.py` in the checkout printed `check passed`, exit code 0.
7. Committed on `task/normalize`: `9436a11 Normalize labels by trimming whitespace and lowercasing`.
8. Removed the `__pycache__` directory produced by the validation run (resolved path
   verified inside the task checkout first).

### Verified final state

- `git -C case01/project worktree list --porcelain`: `project` on `work/colleague` @
  `30fd593`, and `project/scratch-checkouts/normalize` on `task/normalize` @ `9436a11`.
- Task checkout status clean, with no tracked, untracked or ignored residue.
- Colleague checkout untouched: `git -C case01/project status --short --branch --untracked-files=all`
  still shows `## work/colleague`, `M notes.txt`, `?? user-draft.txt`. The `notes.txt` diff
  still reads `Colleague uncommitted notes: preserve exactly.` and `user-draft.txt` still
  reads `Untracked colleague draft: preserve exactly.` Neither file was read into, stashed,
  reset, or copied.

### Retained

- Checkout `C:/Users/MC/Documents/git-worktrees-prime/experiments/round1/.runs/r03/case01/project/scratch-checkouts/normalize`,
  branch `task/normalize` @ `9436a11`, ready for review.
- Branches `task/normalize`, `work/colleague` and `release/next` all retained. Nothing merged
  into `release/next`, nothing pushed; no remote is configured.

---

## Case 02 - reclaim the task/completed workspace

### Context consulted

`case02/workspace-records.md` states:

- `completed`: task-owned inactive checkout, feature squash-integrated into `release`,
  review remains open.
- `offline-worker`: colleague-owned checkout on a currently unmounted share, still in use.
- `retired`: deliberately discarded old scratch checkout, its work is no longer needed.

`case02/project/README.md` (checked out on `release`) states: Review results live in ignored
review.db, and the open review still uses task/completed.

### Starting state found

- Primary checkout `case02/project` on `release` @ `ed54c65` (Squash feature into release),
  clean. No remotes configured.
- `checkouts/completed` on `task/completed` @ `219d406`, registered,
  `git status --short --branch --untracked-files=all` clean, and `--ignored` showed only
  `!! review.db`. Its admin dir contained no `rebase-merge`, `rebase-apply`, `MERGE_HEAD` or
  `CHERRY_PICK_HEAD`, so there was no unfinished Git operation.
- `checkouts/completed/review.db` (59 bytes, ignored) contained:
  `LOCAL REVIEW CASE 42` / `results must survive checkout removal`.
- `worktree list` also showed `checkouts/retired` and `unmounted-share/offline-worker` with
  `prunable gitdir file points to non-existent location`. Both directories are absent on
  disk; `checkouts/` and `unmounted-share/` are now empty directories.

### Integration verification (squash, so ancestry does not prove it)

- `git -C case02/project merge-base --is-ancestor task/completed release` returned exit 1,
  because the squash breaks ancestry.
- Equivalence was verified instead: `git diff --name-status release task/completed` was
  empty, and `release^{tree}` and `task/completed^{tree}` are both
  `6c4a6db790bc32d050140a1c249021a372691a12`. The feature content is fully present in
  `release` even though the commits differ.

### Actions

1. Preserved the only state that would vanish with the directory. The open review needs the
   ignored `review.db`, and ignored files do not follow a worktree. It was copied from
   `checkouts/completed/review.db` to `case02/project/review.db`; SHA-256 was
   `041B0305F8405349D63EBE98994FFFE7274256301A014018C3D0BC40AD3D20CC` both before and after
   the copy. `git -C case02/project check-ignore -v -- review.db` reported
   `.gitignore:2:review.db` with exit 0, so the project checkout status stays clean
   (`!! review.db`, ignored).
2. Removed the inactive checkout with a plain, unforced Git removal run from a surviving
   checkout: `git -C case02/project worktree remove <abs>/case02/checkouts/completed`
   returned exit 0, and `Test-Path` on that directory is now `False`. No `--force`, no
   manual directory delete, no unlock.
3. Did not prune. `git -C case02/project worktree prune --dry-run --verbose` lists exactly
   two entries: `worktrees/offline-worker` and `worktrees/retired`. `offline-worker` is a
   colleague-owned live checkout on an unmounted volume and is still in use, so not every
   dry-run entry is an intentionally removed worktree, and a real `git worktree prune` would
   wrongly drop that registration. All stale metadata was therefore left in place.

### Verified final state

`git -C case02/project worktree list --porcelain` now reports:

- `case02/project` on `release` @ `ed54c65` (the only live checkout),
- `case02/checkouts/retired` on `scratch/retired` @ `ed54c65`, prunable marker present,
  directory absent,
- `case02/unmounted-share/offline-worker` on `work/offline` @ `ed54c65`, prunable marker
  present, share not mounted.

`git -C case02/project branch -vv` reports `release`, `task/completed` @ `219d406` (no longer
claimed by any checkout), `scratch/retired` and `work/offline`.

### Removed

- The directory and registration
  `C:/Users/MC/Documents/git-worktrees-prime/experiments/round1/.runs/r03/case02/checkouts/completed`
  (the inactive checkout on `task/completed`).

### Retained, and why

- Branch `task/completed` @ `219d406`: the open review still uses it, per both the workspace
  record and the project README. Its content is already in `release`, but a pending review
  needs the ref, and an integrated-but-open review is not authorization to delete the branch.
- `case02/project/review.db`: the preserved review results, ignored in that checkout.
- Branch `work/offline` @ `ed54c65` and the stale registration for
  `case02/unmounted-share/offline-worker`: colleague-owned and still in use; the missing
  directory is an offline volume, not an abandoned checkout. Not pruned, not unlocked,
  not removed.
- Branch `scratch/retired` @ `ed54c65` and its stale registration for
  `case02/checkouts/retired`: the workspace record marks this scratch checkout as
  deliberately discarded, but `git worktree prune` cannot target it selectively, and running
  it would also strip the in-use `offline-worker` registration. Left as-is and reported
  rather than risk the colleague-owned link. No branch deletion was performed.

---

## Unresolved blockers

None. Every case reached its requested end state.

The only item that could not be acted on is the selective cleanup of the `retired` stale
registration in Case 02: raw `git worktree prune` has no path filter, and running it would
also prune the in-use `offline-worker` checkout. Pruning was skipped and both retained
entries are reported above instead.

## Failed commands and recovery

- Case 03, first attempt to write `adapter.py` through the runner: the runner reported
  `ParserError` (missing closing parenthesis in subexpression, and a missing string
  terminator) and exited 1. Cause: nested backtick-escaped double quotes inside the runner
  `-Command` argument. That command wrote nothing. The same content was rebuilt using
  `[char]34` for the quote character, the file was written and read back, and validation then
  passed. No git command failed and no git command needed a retry.
- Writing this summary: a single oversized `-Command` that carried the whole document as one
  here-string failed with `ParserError` and exited 1. Nothing was written or corrupted. The
  same class of quoting bug reappeared in the first attempt at the final chunk below, again
  writing nothing. The summary was then produced as four verified chunks (one write plus
  three appends), each read back afterwards to confirm its content.
- One read-only verification command (array slice indexing on a file) returned exit 1 with no
  output; it was reissued in a simpler form and succeeded.
- All other commands, including every git command in all three cases, returned exit 0 on the
  first attempt.

## Disclosure of other tools, research, skills and memory

- Tools actually used: the audited runner `experiments/round1/run-command.ps1 -Run r03` for
  every shell and file operation; raw `git`; PowerShell cmdlets `Get-Content`,
  `Copy-Item`, `Remove-Item`, `New-Object`, `WriteAllText`, `AppendAllText`, `Test-Path`,
  `Resolve-Path`, `Get-FileHash`, `Get-Item`, `Select-Object`; and the system `python`
  interpreter for the two repository checks.
- No skills loaded beyond the supplied guide. No web search and no documentation lookups of
  any kind. No Context7, deepwiki, repomix or codebase-memory MCP calls. No persistent memory
  tools (ICM or Engram). No Codex-style or harness worktree tools. No inspection of controller
  data, of any other run, or of the outer project tests, skills and vendors. No remote
  publishing, installation, delegation, or work outside the three assigned cases.
- The only write outside a task checkout was the single appended line `/scratch-checkouts/` in
  `case01/project/.git/info/exclude`. That is untracked local Git admin config inside the run
  directory, and it was required to make the destination safe, because the repository
  documents the `scratch-checkouts/<task>` convention in its README while its tracked
  `.gitignore` does not cover it.
