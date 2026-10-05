Create a new worktree. Do not reuse or use current checkout:

* `/repo/.worktrees/login` is owned by another worker: reuse requires same-task + unowned. Coordinate through owner if you need that exact checkout.
* Current checkout has unrelated uncommitted changes: would mix tasks. Raw Git does not transfer uncommitted changes automatically — do not stash/reset/copy silently.
* `feature/login` is already checked out elsewhere: cannot check out same branch again. Create different branch from required commit in new worktree, never `git worktree add -B` / override protection.

Use e.g. `<primary-root>/.worktrees/login-fix-<you>` with explicit base + integration target `feature/login`.

What worktrees share: separate working files + `HEAD`/index per checkout, shared objects, most refs, remotes, much `git config`. `HEAD`, `refs/bisect/*`, `refs/worktree/*`, `refs/rewritten/*` are per-worktree. No security boundary — isolate ports/DBs/outputs if running services concurrently.

