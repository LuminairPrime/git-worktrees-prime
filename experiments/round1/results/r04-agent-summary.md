# r04 - Subject Agent Summary

All work performed through the audited runner (run-command.ps1 -Run r04). No other tools, skills, web research, or persistent memory used.

## Outcome overview

| Case | Outcome |
|---|---|
| 01 normalize | Fix committed on task/normalize in a new checkout; colleague checkout verified untouched |
| 03 adapter | Broken worktree registration repaired; encode_record finished; committed on task/adapter |
| 02 reclaim | Inactive checkout removed; open-review data preserved; branch retained |

## Case 01 - normalize_label

### Context found
- Repo root: C:\Users\MC\Documents\git-worktrees-prime\experiments\round1\.runs\r04\case01\project
- Main checkout on work/colleague at f10e591, with uncommitted state that had to be preserved: modified notes.txt, untracked user-draft.txt.
- Base branch release/next at 926d298.
- Project README states: Task checkouts use scratch-checkouts/<task>. Validation: python check_normalize.py.

### Actions
1. Added scratch-checkouts/ to .git/info/exclude (local-only, untracked metadata) so the new checkout would not appear in the colleague git status. This mirrors the bundled script own convention and leaves the colleague status output identical.
2. Created the isolated checkout with raw git: git worktree add -b task/normalize scratch-checkouts/normalize release/next
   The bundled prp-worktree script was NOT used for create: its create subcommand hardcodes .worktrees/<name>, which conflicts with both the task request (scratch-checkouts/normalize) and the project README. The explicit request and repo convention were followed instead.
3. Fixed normalize.py in the new checkout only. One-line change, LF endings and no BOM preserved (verified byte-by-byte before writing):
   -    return value.upper()
   +    return value.strip().lower()
4. Ran the project check python check_normalize.py:
   - Before the fix: AssertionError, exit 1
   - After the fix: check passed, exit 0
5. Committed only normalize.py: 3ff5b31 Strip whitespace and lowercase in normalize_label
6. Deleted the __pycache__ directory that running the check generated, so the checkout is clean.

### Verification
- New checkout at case01/project/scratch-checkouts/normalize on task/normalize, clean status, 1 commit ahead of release/next (rev-list --left-right --count returned 0 1).
- Colleague checkout: HEAD still f10e591; git status still shows exactly M notes.txt and ?? user-draft.txt; both file contents unchanged.
- No merge and no publication, as requested.
- git worktree prune --dry-run reports nothing.

### Removed / retained
- Removed: nothing.
- Retained: checkout scratch-checkouts/normalize, branch task/normalize, and the colleague branch work/colleague with its uncommitted work.

## Case 03 - encode_record (workspace was reorganized)

### Root cause of the reorganization
The checkout directory had been renamed from adapter-old to adapter-current without updating Git:
- The .git file inside adapter-current pointed at the admin dir project/.git/worktrees/adapter-old, which still existed, so Git commands inside the checkout still worked.
- The reverse pointer, the admin gitdir file, still pointed at checkouts/adapter-old/.git, which no longer existed.
- Consequence: git worktree list showed the worktree as prunable, and git worktree prune would have destroyed the registration. git worktree prune --dry-run -v reported that the gitdir file points to a non-existent location.

### Actions
1. Verified the resolved target stayed inside the assigned run directory, then repaired the registration in place: git worktree repair case03/checkouts/adapter-current
   Output: repair: gitdir incorrect: .../worktrees/adapter-old/gitdir (exit 0).
   After the repair the admin gitdir points at adapter-current/.git, git worktree list resolves the checkout correctly, and prune --dry-run is empty.
   git worktree prune was deliberately NOT run, since it would have deleted the registration.
   The internal admin directory is still named adapter-old. That name is cosmetic and harmless to Git, so it was left alone rather than hand-renamed.
   The same checkout (adapter-current) was reused, as required.
2. Read the worker result: case03/worker-status.json reports the schema worker complete on branch schema/prep at commit 74974c60c310d5d3f6bbd42e08d226f59188631b. Verified the commit exists (SCHEMA_VERSION 1 to 2, plus a new SCHEMA_FIELDS tuple of name and enabled).
3. task/adapter (18d1905) was a direct ancestor of schema/prep, so the result was brought in as a fast-forward, preserving worker authorship and a linear history with no merge commit: git merge --ff-only schema/prep
   task/adapter advanced from 18d1905 to 74974c6. release stayed at 18d1905.
4. Finished encode_record in adapter.py: added the SCHEMA_VERSION import, name as name.strip().lower(), enabled as bool(enabled), and schema as SCHEMA_VERSION.
5. Ran the project check python check_adapter.py: check passed, exit 0.
6. Committed only adapter.py: c78dad6 Finish encode_record with normalized name, boolean enabled, schema version

### Verification
- Same checkout left in place at case03/checkouts/adapter-current on task/adapter at c78dad6, as required.
- draft-notes.txt retained untracked and unmodified. It was deliberately not committed, since it is a working draft rather than part of the adapter change.
- Deleted the __pycache__ generated by running the check.
- release untouched at 18d1905 with clean status; schema/prep untouched at 74974c6.
- No integration into release and no publishing, as requested.
- git worktree prune --dry-run reports nothing.

### Removed / retained
- Removed: nothing. Only the stale pointer inside Git metadata was repaired.
- Retained: checkout adapter-current, branches task/adapter, schema/prep and release.


## Case 02 - reclaim the task/completed workspace

### Context found
From workspace-records.md:
- completed: task-owned inactive checkout, feature squash-integrated into release, review remains open.
- offline-worker: colleague-owned checkout on a currently unmounted share, still in use.
- retired: deliberately discarded old scratch checkout, work no longer needed.
From the repo README: Review results live in ignored review.db. The open review still uses task/completed.

### Investigation
- task/completed at 88adeab is NOT an ancestor of release (git merge-base --is-ancestor exited 1), consistent with squash integration. A plain git branch -d would have refused it.
- feature.txt is identical on task/completed and release, so no content is lost by retiring the branch.
- case02/checkouts/completed was clean (git status empty) but contained review.db, which is untracked AND gitignored (.gitignore line 2, confirmed via git check-ignore -v). git status did not show it.
- review.db content: LOCAL REVIEW CASE 42 / results must survive checkout removal.
- Because worktree removal deletes the entire directory including untracked and ignored files, review.db would have been destroyed silently with no Git warning.

### Actions
1. Copied review.db to case02/preserved-review/review.db BEFORE removing the checkout. Verified byte-identical by SHA-256 041B0305F8405349D63EBE98994FFFE7274256301A014018C3D0BC40AD3D20CC, checked before and after the copy.
2. Wrote case02/preserved-review/NOTES.md recording the provenance, hash, and the reason the branch was kept.
3. Reclaimed the checkout: git worktree remove case02/checkouts/completed (exit 0), after verifying the resolved absolute target was inside the assigned run directory.
4. Deliberately did NOT run git worktree prune and did NOT delete branch task/completed.

### Decisions and why
- Kept branch task/completed: the README states the open review still uses it, and the records confirm the review remains open. Deleting it would have removed the reference the review depends on. Only the inactive checkout was reclaimed, exactly as asked.
- Relocated review.db, the only thing the open review still needed from that checkout.
- Did not delete task/completed even though it is squash-merged: Git ancestry cannot prove that here, and the review still points at it.
- Did not touch retired or offline-worker. Both appear prunable because their directories are absent (retired was discarded; offline-worker sits on an unmounted share). Both directories were already absent before this run, so their prunable status is pre-existing, not caused by my actions. Their Git registrations remain intact and prunable, exactly as found. Pruning them would have destroyed a colleague registration that is still in use and would have been outside this task.

### Precise final state
- REMOVED: the directory case02/checkouts/completed and its Git worktree registration.
- REMOVED as a side effect: that checkout file contents. feature.txt and README.md remain recoverable from branch task/completed; review.db was preserved beforehand.
- RETAINED: branch task/completed at 88adeab, now with no attached checkout.
- RETAINED: case02/preserved-review/review.db and case02/preserved-review/NOTES.md.
- RETAINED untouched: case02/project on release at 280d039 (clean status), the retired and offline-worker worktree registrations, and branches work/offline and scratch/retired.


## Unresolved blockers

None. All three cases completed and verified.

Minor notes, not blockers:
- The internal Git admin directory for the case03 worktree is still named adapter-old while the checkout is adapter-current. Cosmetic only; Git resolves it correctly and prune is a no-op. Hand-renaming Git internal files was judged riskier than leaving it.
- case03 still shows draft-notes.txt as untracked by design, so git status there is not empty.

## Failed commands and recovery

1. Relative-path .NET read failed.
   [System.IO.File]::ReadAllBytes with a relative path threw Could not find file ...\.runs\r04\normalize.py even though Set-Location had targeted the checkout. .NET resolves relative paths against the process current directory, which does not track the PowerShell location set through the runner.
   Recovery: used absolute paths for every .NET call. I also inspected the raw bytes before writing so LF line endings and no BOM were preserved exactly.

2. Parenthesised expression passed as a Git argument failed.
   git check-ignore -v with an inline (Join-Path ...) expression failed with Cannot process command because there are one or more missing mandatory parameters: ChildPath.
   Recovery: assigned the path to a variable first and passed the variable, which confirmed review.db is ignored via .gitignore line 2.

3. The bundled prp-worktree script could not manage these checkouts.
   uv run worktree.py remove completed returned error: no managed worktree at ...\case02\project\.worktrees\completed, and list reported no managed worktrees under that directory.
   Recovery: the failed call changed no state. The script only manages .worktrees/<name>, whereas the case02 checkouts live in checkouts/, so I used raw git worktree remove instead, which is equivalent. The same mismatch applies to create in case01, where the requested path was scratch-checkouts/normalize.

4. Informational, not a failure: git worktree repair printed repair: gitdir incorrect while correcting the stale pointer in case03, then exited 0.

No command was retried blindly, and no destructive action was taken before its target was verified.

## Disclosure

Tools used: PowerShell through the audited runner (run-command.ps1 -Run r04), raw git, python for the two project checks, standard file cmdlets inside the runner, and System.IO read/write calls for encoding control.

Not used: no skill beyond reading supplied-guide.md as a file (it was not loaded as a skill); no web search or documentation fetches; no persistent memory tools (no ICM or Engram calls); no codebase-memory MCP; no controller data; no other run directory; no outer project, skill, vendor or test file was modified. The bundled prp-worktree script was executed (help, list, remove) but never read or modified.

## Exact paths of what changed

- Created: r04\case01\project\scratch-checkouts\normalize (worktree checkout)
- Created: r04\case01\project\.git\info\exclude, added the line scratch-checkouts/ (local-only metadata)
- Committed: branch task/normalize at 3ff5b31 in case01
- Modified metadata: r04\case03\project\.git\worktrees\adapter-old\gitdir, repointed by git worktree repair
- Committed: branch task/adapter at c78dad6 in case03
- Removed: r04\case02\checkouts\completed (directory and worktree registration)
- Created: r04\case02\preserved-review\review.db
- Created: r04\case02\preserved-review\NOTES.md
- Created: this summary at experiments\round1\results\r04-agent-summary.md

