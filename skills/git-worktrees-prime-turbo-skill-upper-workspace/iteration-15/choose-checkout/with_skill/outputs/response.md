Create a new worktree — do not reuse or use current checkout.

* Do not reuse `/repo/.worktrees/login`: owned by another worker. Reuse only if no other worker owns it. Do not clean, pull into, or integrate in another worker's checkout.
* Do not work in current checkout: unrelated uncommitted changes require separation, and `feature/login` is already checked out elsewhere.
* Create at unused path, e.g. `<primary-root>/.worktrees/login-<task>`: unique task name, not inside another disposable worktree. Verify with `git worktree list --porcelain -z`.

Branch constraint: cannot checkout `feature/login` twice. Coordinate with owner to reuse, or create different branch from same commit, e.g. `feature/login-fix`. Never force with `-B` / override checkout protection. Uncommitted changes do not transfer automatically — transfer deliberately.

What worktrees share: separate working files/`HEAD`/index, but share objects, most refs, remotes, much config. `HEAD`, `refs/bisect/*`, `refs/worktree/*`, `refs/rewritten/*` are per-worktree. No security boundary — also isolate ports/DBs/outputs.

