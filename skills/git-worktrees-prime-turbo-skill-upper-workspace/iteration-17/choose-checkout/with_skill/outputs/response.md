Create a new worktree — do not reuse `/repo/.worktrees/login` and do not work in current checkout.

* **Do not reuse:** that checkout belongs to another worker. Reuse only if no other worker owns it.
* **Do not use current checkout:** unrelated uncommitted changes require separation, and `feature/login` is already checked out elsewhere — never override checkout protection.
* **Create:** new unused path, e.g. `<primary-root>/.worktrees/login-fix`, with a different branch from the required commit, e.g. `fix/login-<bug>`, keeping path, branch, base commit, and integration target explicit. Uncommitted changes do not transfer automatically.

Worktrees share objects, most refs, remotes, and much Git config; they separate working files and indexes. `HEAD`, `refs/bisect/*`, `refs/worktree/*`, `refs/rewritten/*` are per-worktree. No security boundary — coordinate shared refs and use distinct ports/DBs/outputs.

