Create a new worktree. Don't reuse or use current checkout.

* Don't reuse `/repo/.worktrees/login`: owned by another worker. Don't clean, remove, pull into, or override branch checkout in another worker's checkout. Reuse only through its owner.
* Don't use current checkout: unrelated uncommitted changes require separation. Raw worktree changes don't transfer automatically — don't stash/reset/copy silently.
* New checkout needs a different branch: `feature/login` is already checked out elsewhere, so create e.g. `feature/login-<fix>` from required base commit at a unique unused path, verified via `git worktree list --porcelain -z`.

Worktrees share: objects, most refs, remotes, much Git config. They separate: working files, index/staging, `HEAD`, `refs/bisect/*`, `refs/worktree/*`, `refs/rewritten/*`. No security boundary — coordinate shared mutations, plus separate ports/DBs/outputs if running services.
