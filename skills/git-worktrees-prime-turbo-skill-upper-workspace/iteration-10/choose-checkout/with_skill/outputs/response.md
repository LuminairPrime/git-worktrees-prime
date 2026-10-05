Create a new worktree — do neither of the other options:

* **Don't reuse `/repo/.worktrees/login`:** owned by another worker. Per rule: reuse only if no other worker owns it. Don't clean/remove/relocate another worker's checkout, don't `pull` into it, coordinate through owner.
* **Don't work in current checkout:** has unrelated uncommitted changes. That requires separation. Raw-Git changes don't follow automatically — don't silently stash/reset/copy.

New path: unique unused path, e.g. `<primary-root>/.worktrees/login-fix-<you>` — not inside another disposable worktree. Verify with `git worktree list --porcelain -z`.

Branch caveat: `feature/login` is already checked out in the other worktree. You cannot check out the same branch in two worktrees. Either coordinate to reuse that checkout via owner, or create a different branch from same base/commit for your fix. Never force with `-B` / override checkout protection.

What worktrees share:
* **Separate:** working files, index/staging area, `HEAD`, `refs/bisect/*`, `refs/worktree/*`, `refs/rewritten/*`.
* **Shared:** objects, most refs/branches, remotes, much Git config.
* No security boundary — use distinct ports/DBs/outputs if running services concurrently.

