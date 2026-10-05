Create a new worktree. Do not reuse `/repo/.worktrees/login` and do not use current checkout.

* Reuse fails rule 1: existing checkout belongs to this task only if no other worker owns it. That one is owned — do not pull into, clean, or remove another worker's checkout. `feature/login` is also already checked out there, Git will block a second checkout of same branch.
* Current checkout fails rule 2: unrelated uncommitted changes require separation. They do not transfer automatically, do not stash/reset/copy them silently.

Do: `git worktree list --porcelain -z` to confirm registrations, then create at unused path e.g. `<primary-root>/.worktrees/login-<you>` from same base commit on a different branch e.g. `feature/login-fix-<you>`, or coordinate with owner to reuse theirs.

Worktrees share: objects, most refs, remotes, much Git config.
Worktrees separate: working files, index, `HEAD`, `refs/bisect/*`, `refs/worktree/*`, `refs/rewritten/*`.
No security boundary: also separate ports, DBs, outputs if running services.

