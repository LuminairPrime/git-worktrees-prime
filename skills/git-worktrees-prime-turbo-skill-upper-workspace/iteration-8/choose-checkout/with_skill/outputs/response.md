Create a new worktree. Do not reuse `/repo/.worktrees/login` and do not work in current checkout.

* Owned by another worker: reuse only if no other worker owns it. Confirm via `git worktree list --porcelain -z`. Never clean/take over another worker's checkout.
* Current checkout has unrelated uncommitted changes: concurrent edits/conflicting branch/unrelated changes require separation.
* Same branch `feature/login` already checked out: cannot checkout twice. Reuse through owner or create different branch from same commit. Never use `git worktree add -B` to override.

New path: unused path e.g. `<primary-root>/.worktrees/<task-unique>`, not inside another disposable worktree, verify ignore coverage.

Worktrees share: objects, most refs, remotes, much Git config. Separate: working files, index, `HEAD`, `refs/bisect/*`, `refs/worktree/*`, `refs/rewritten/*`. No security boundary; isolate ports/DBs/outputs too. Uncommitted changes do not follow automatically.

