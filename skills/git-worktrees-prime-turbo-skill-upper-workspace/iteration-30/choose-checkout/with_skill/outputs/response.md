Create a new worktree — do not reuse `/repo/.worktrees/login` and do not work in current checkout.

* Owned by another worker: per rule 1, reuse only if no other worker owns it. Do not clean / pull into someone else's checkout, never override checkout protection — `feature/login` is already checked out there.
* Current checkout has unrelated uncommitted changes: per rule 2, conflicting branch + dirty state requires separation. Changes do not follow a new worktree automatically, do not stash/reset/copy blindly.

Fix: create ` <primary-root>/.worktrees/<task-unique>` — unique unused path, not inside another disposable worktree — with a different branch from `feature/login` commit, e.g. `feature/login-fix-<id>`. If you must use same branch name, coordinate reuse through owner.

Worktrees share: objects, most refs, remotes, much Git config. Separate: working files, index/staging, `HEAD`, `refs/bisect/*`, `refs/worktree/*`, `refs/rewritten/*`. No security boundary — also separate ports/DBs/outputs.

