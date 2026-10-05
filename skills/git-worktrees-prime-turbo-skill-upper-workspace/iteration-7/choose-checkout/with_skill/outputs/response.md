Create a new worktree. Do not reuse or use current checkout:

* ` /repo/.worktrees/login` is owned by another worker: reuse requires same-task + unowned. Reusing risks dirty state, conflicts, `git worktree list` ownership confusion. Do not `pull` / `reset` / `clean` in it.
* Current checkout has unrelated uncommitted changes: would mix tasks. Raw Git does not auto-transfer changes.
* Same branch cannot be checked out twice: `feature/login` is already checked out at `/repo/.worktrees/login`. Never override with `-B` / force. Create different task branch from `feature/login` commit, e.g. `<primary-root>/.worktrees/login-fix` with `feature/login-fix`.

What worktrees share:

* Share: objects, most refs, remotes, much Git config.
* Per-worktree: working files, index/staging, `HEAD`, `refs/bisect/*`, `refs/worktree/*`, `refs/rewritten/*`.
* No security boundary: also separate ports, DBs, outputs if running services.

