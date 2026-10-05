Create a new worktree. Do not reuse or work in current checkout.

* Don't reuse `/repo/.worktrees/login`: owned by another worker. Never clean, remove, or take over another worker's checkout.
* Don't use current checkout: unrelated uncommitted changes require separation. Mixing would force stash/reset and risk cross-contamination.
* New path: unique unused path, e.g. `<primary-root>/.worktrees/login-fix`, not inside another worktree.

Caveat: `feature/login` is already checked out elsewhere, so you cannot check it out again. Reuse through owner, or create different branch from same commit, e.g. `fix/login-bug` from `feature/login`. Never override checkout protection with `-B`.

What worktrees share:

* Separate: working files, index/staging, `HEAD`.
* Per-worktree refs: `refs/bisect/*`, `refs/worktree/*`, `refs/rewritten/*`.
* Shared: objects, most refs/branches, remotes, much `git config`.
* No security boundary: also separate ports, DBs, outputs if running services.

