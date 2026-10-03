# Run r01 agent summary - Case 01
## Actions per case

Case 01 - active checkout repair and finish:
- Listed worktrees with git worktree list porcelain from case01/project primary checkout.
- Confirmed stale registration at case01/checkouts/active while live directory is at case01/checkouts/active-live.
- Verified live checkout branch task/active tip 49ffb35 and untracked draft-notes.txt present.
- Repaired with git worktree repair using absolute path to active-live.
- Verified repair: gitdir now points to active-live dot git and list shows active-live registered.
- Edited case01/checkouts/active-live/app.py to return 2 with LF ending.
- Ran python check_app.py in active-live: check passed.
- Removed generated __pycache__ so only draft-notes.txt remains untracked.
- Committed only app.py on task/active with message Finish version to return 2.
- New tip 6af4199 verified with log and status clean except draft-notes.txt.

Case 01 - retired checkout reclaim:
- Inspected retired admin gitdir and confirmed checkout directory missing.
- Verified scratch/retired tip 10c9c92 is ancestor of release with merge-base is-ancestor exit 0.
- Checked workspace-records: retired is deliberately discarded, work no longer needed.
- Removed only retired registration with git worktree remove on its exact old path.
- Verified list no longer shows retired and prune dry-run then shows only offline-worker.
- Did not run blanket prune because offline-worker must be retained.

## Tests run
- python check_app.py in active-live before fix would fail, after fix reports check passed twice.
- git worktree list porcelain before and after repair and after retired removal.
- git status short branch with untracked-files all in active-live and primary.
- git status short ignored in both checkouts.
- git rev-parse HEAD and branch show-current in active-live.
- git merge-base is-ancestor scratch/retired release exit 0.
- git worktree prune dry-run verbose before and after.
- git branch vv and git log oneline all graph.

## Exact paths branches removed retained
- Repaired: C:/Users/MC/Documents/git-worktrees-prime/experiments/round4/.runs/r01/case01/checkouts/active-live on branch task/active from tip 49ffb35 to 6af4199.
- Retained untracked: case01/checkouts/active-live/draft-notes.txt with content Active draft notes keep exactly.
- Removed checkout registration only: C:/Users/MC/Documents/git-worktrees-prime/experiments/round4/.runs/r01/case01/checkouts/retired.
- Retained branch scratch/retired at 10c9c92, no checkout now, work verified integrated and authorized discard.
- Retained checkout registration and branch work/offline at C:/Users/MC/Documents/git-worktrees-prime/experiments/round4/.runs/r01/case01/unmounted-share/offline-worker.
- Retained primary: C:/Users/MC/Documents/git-worktrees-prime/experiments/round4/.runs/r01/case01/project on release with M notes.txt WIP line and untracked draft.yaml.
- Retained stash entry On release colleague-hotfix, left untouched.
- Retained task/active branch with history 10c9c92, 49ffb35, 6af4199.

## Unresolved blockers
- None. All assigned steps completed and verified.

## Failed commands and recovery
- One stash show with unquoted stash ref failed parsing due to PowerShell hashtable syntax. No state changed. Recovered by using stash list only for verification and leaving stash untouched.
- Initial app.py edit added extra blank line and CRLF. Recovered by rewriting file with LF ending to minimal diff, re-ran check, cleaned cache, then committed.

## Disclosure of tools research skills memory
- Used only supplied-guide.md and TASKS.md plus workspace-records.md for context.
- Used only raw Git and Python via audited runner. No harness worktree tools.
- Did not load other skills, did not use web search, did not read outer docs or setup scripts.
- Did not use persistent memory tools ICM or Engram or codebase-memory MCP.
- Did not touch other runs or controller data. All operations stayed inside r01 case01.
- All shell and file operations went through run-command.ps1 with Run r01.
