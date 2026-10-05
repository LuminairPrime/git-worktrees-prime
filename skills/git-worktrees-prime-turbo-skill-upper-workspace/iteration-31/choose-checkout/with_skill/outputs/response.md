Create a new worktree. Do not reuse or use current checkout:

* ` /repo/.worktrees/login`: owned by another worker — reuse only if no other worker owns it. Do not clean / remove / take over another worker's checkout.
* Current checkout: has unrelated uncommitted changes — concurrent edits / conflicting branches / unrelated changes require separation.
* Same branch cannot be checked out twice: `feature/login` is already checked out in that worktree. Create different branch from same commit in new worktree, or coordinate with owner to reuse theirs. Never override with `git worktree add -B`.

New path: unique unused path, e.g. `<primary-root>/.worktrees/login-<task>` — not inside another disposable worktree, verified with `git worktree list --porcelain -z`. Uncommitted changes do not follow automatically.

What worktrees share:
* Separate: working files, index, `HEAD`, `refs/bisect/*`, `refs/worktree/*`, `refs/rewritten/*`.
* Share: objects, most refs, remotes, much Git config. No security boundary — also isolate ports/DBs/outputs.

