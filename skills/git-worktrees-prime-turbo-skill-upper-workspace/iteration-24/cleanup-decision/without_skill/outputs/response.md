Checked in order — stopped at check 1:

1. Locate main repo and worktree: `/repo` not found, `/repo/.worktrees/old-task` not found. `git rev-parse --show-toplevel` in current dir: not a git repo. `git worktree list`: no repo. Cannot remove/delete/prune — nothing to act on.

Full order I would run if path existed:

1. `pwd` — confirm you are not inside `/repo/.worktrees/old-task` to be removed.
2. `git worktree list --verbose` — confirm worktree registered and not `locked`.
3. `git -C /repo/.worktrees/old-task status --porcelain` — must be empty. Save/stash any output first. `remove` will refuse with uncommitted changes.
4. Verify squash-merge: `git branch --merged main` will *not* list it — expected for squash. Check instead: `git cherry main...<branch>` (empty = upstream equivalent), or PR shows `Merged`, plus `git log --oneline main --grep=<squash-commit>`. Do not use this to auto-delete.
5. Only then: `git worktree remove /repo/.worktrees/old-task` — use `--force` only if step 3 intentionally discarded.
6. `git worktree list` — confirm gone, then delete branch: `git branch -d <branch>` will fail for squash; after step 4 confirmation use `git branch -D <branch>`.
7. `git worktree prune --verbose; git worktree list; git fetch --prune` — final cleanup.

Provide correct repo path or output of `git worktree list --verbose` from main checkout and I will walk the rest.
