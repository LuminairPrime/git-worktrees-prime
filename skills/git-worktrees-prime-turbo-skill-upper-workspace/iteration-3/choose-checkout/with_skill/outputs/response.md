Create a new worktree. Do not reuse `/repo/.worktrees/login` and do not work in current checkout.

* Owned by another worker: reuse only if no other worker owns it. Coordinate via owner if you must use that checkout.
* Current checkout has unrelated uncommitted changes: requires separation. Uncommitted changes do not follow a raw `git worktree add` automatically — do not stash/reset/bulk-copy them.
* `feature/login` is already checked out elsewhere: Git will refuse a second checkout of same branch. Create different branch from required commit e.g. `<primary-root>/.worktrees/login-<task>` with `-b <new-branch>`, or detached `HEAD` for inspection only. Never use `-B` to override.

What worktrees share: separate working files + index/`HEAD` per checkout, but share objects, most refs, remotes, much config. Per-worktree only: `HEAD`, `refs/bisect/*`, `refs/worktree/*`, `refs/rewritten/*`. No security boundary — also isolate ports/DBs/outputs.

