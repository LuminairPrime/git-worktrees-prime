Create a new worktree. Don't reuse `/repo/.worktrees/login` and don't work in current checkout.

* `login` worktree is owned by another worker: reuse only if no other worker owns it. Do not clean, remove, or take over another worker's checkout without coordination.
* Current checkout has unrelated uncommitted changes: requires separation to avoid mixing tasks. Uncommitted changes don't follow a new worktree automatically — transfer only what's needed.
* `feature/login` is already checked out elsewhere: Git checkout protection blocks checking out the same branch twice. Reuse through owner, or create a different branch from same commit, e.g. `fix/login-bug` from `feature/login`. Never force with `-B`/`--force`.

New path: unique unused path per convention, e.g. `<primary-root>/.worktrees/login-fix`, not inside another disposable worktree.

What worktrees share/separate:

* Separate: working files, index/staging, `HEAD`.
* Per-worktree refs: `refs/bisect/*`, `refs/worktree/*`, `refs/rewritten/*`.
* Shared: objects, most refs/branches, remotes, much Git config. Coordinate fetches/pushes/branch moves.
* No security boundary; also separate ports, DBs, build outputs if running concurrently.

