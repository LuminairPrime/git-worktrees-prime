Create a new worktree, do not reuse or use current checkout:

* Do not reuse `/repo/.worktrees/login`: owned by another worker. Reuse requires owner coordination, and `feature/login` already checked out there cannot be checked out again elsewhere. Never override checkout protection.
* Do not use current checkout: unrelated uncommitted changes require separation. Raw `git worktree add` does not transfer uncommitted changes.
* Create task worktree at unused path e.g. `<primary-root>/.worktrees/login-fix-<you>` from same base commit, with different branch e.g. `feature/login-fix-<you>` or detached `HEAD` for inspection.

Worktrees share: objects, most refs, remotes, much Git config. Separate: working files, index, `HEAD`, `refs/bisect/*`, `refs/worktree/*`, `refs/rewritten/*`. No security boundary — also isolate ports/DBs/outputs.

