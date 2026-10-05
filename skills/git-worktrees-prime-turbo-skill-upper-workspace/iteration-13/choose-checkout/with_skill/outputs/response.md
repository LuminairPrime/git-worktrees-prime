Create a new worktree. Do not reuse `/repo/.worktrees/login` or work in the current checkout.

* **Do not reuse:** owned by another worker. Reuse requires no other owner and verification via `git worktree list --porcelain -z`, changes, and ongoing operations. Reuse would hit branch checkout protection for `feature/login` and risk racing dirty state.
* **Do not use current checkout:** has unrelated uncommitted changes. That is exactly the concurrent-edits / conflicting-branch / unrelated-changes case that requires separation. Uncommitted changes do not follow a new worktree automatically — do not stash/reset/copy them silently.
* **Create:** use unused path, e.g. `<primary-root>/.worktrees/login-<task>` — not inside another disposable worktree. Since `feature/login` is checked out elsewhere, either coordinate with the owner to reuse that checkout, or create a different branch from the required commit. Never override checkout protection with `-B` / `--force`.

What worktrees share:

Separate: working files, index, `HEAD`.
Shared: objects, most refs, remotes, much Git config.
Per-worktree: `HEAD`, `refs/bisect/*`, `refs/worktree/*`, `refs/rewritten/*`. Coordinate shared mutations. No security boundary — also isolate ports, DBs, outputs if running services.

