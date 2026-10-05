Create a new worktree. Do not reuse `/repo/.worktrees/login` and do not work in current checkout.

* Reuse fails rule 1: checkout belongs to this task only if no other worker owns it. That path is owned by another worker — do not remove, relocate, clean, or pull into it. Coordinate if you need its state.
* Current checkout fails rule 2: unrelated uncommitted changes require separation. Raw `git worktree add` does not transfer them; do not stash/reset/copy silently.
* `feature/login` is already checked out elsewhere, so Git checkout protection blocks checking out the same branch twice. Create a different path with either a new fix branch from the same commit, e.g. `feature/login-fix`, or detached `HEAD` for inspection only.

Use `<primary-root>/.worktrees/<task-unique>`, unused path, not inside another disposable worktree. Verify with `git worktree list --porcelain -z`.

What worktrees share: separate working files, `HEAD`, and index, but share objects, most refs, remotes, and much Git config. `HEAD`, `refs/bisect/*`, `refs/worktree/*`, `refs/rewritten/*` are per-worktree. No security/isolation boundary — separate ports/DBs/outputs if running services.

