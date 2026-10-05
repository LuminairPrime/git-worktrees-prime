Create a new worktree — do not reuse `/repo/.worktrees/login` or use current checkout:

* `feature/login` is already checked out at `/repo/.worktrees/login` owned by another worker: reuse only if no other worker owns it. Never override checkout protection with `-B` / force. Coordinate via owner or use a different branch from same commit.
* Current checkout has unrelated uncommitted changes: requires separation. Raw `git worktree add` does not transfer uncommitted changes; do not stash/reset/copy silently.

New path e.g. `<primary-root>/.worktrees/<task>-<you>` — unique unused path, verify with `git worktree list --porcelain -z`.

Worktrees share: objects, most refs, remotes, much Git config. Separate: working files, index/staging, `HEAD`, `refs/bisect/*`, `refs/worktree/*`, `refs/rewritten/*`. No security boundary — also isolate ports/DBs/outputs.

