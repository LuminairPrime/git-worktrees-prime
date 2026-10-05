Create a new worktree. Do not reuse `/repo/.worktrees/login` or use the current checkout.

* **Do not reuse:** owned by another worker, and `feature/login` is already checked out there. Git checkout protection prevents the same branch in two worktrees. Reuse only through its owner.
* **Do not use current checkout:** unrelated uncommitted changes would mix with the fix. Uncommitted changes do not transfer automatically to a new worktree.
* **Action:** verify with `git worktree list --porcelain -z`, then `git worktree add -b <new-task-branch> <primary-root>/.worktrees/<unique-task> <base-ref>` at an unused path. Do not place inside another disposable worktree. If `feature/login` must be continued, coordinate with owner or branch from the required commit under a different name.

Worktrees share/separate:

* Separate: working files, index/staging area, `HEAD`.
* Shared: objects, most refs, remotes, much Git config.
* Per-worktree only: `HEAD`, `refs/bisect/*`, `refs/worktree/*`, `refs/rewritten/*`. Coordinate shared ref/config mutations. No security boundary.

