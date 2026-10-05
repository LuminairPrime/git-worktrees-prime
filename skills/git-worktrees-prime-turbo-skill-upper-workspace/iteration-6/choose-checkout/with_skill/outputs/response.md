Create a new worktree. Do not reuse `/repo/.worktrees/login` and do not work in the current checkout.

* Reuse? No: that checkout is owned by another worker. Do not work in, pull into, reset, clean, or remove another worker's checkout. Coordinate through its owner if you need that exact checkout.
* Current checkout? No: unrelated uncommitted changes require separation. Raw Git does not transfer them automatically, and mixing them with the `feature/login` fix risks contamination.
* New worktree: Yes — concurrent task + dirty current checkout = separate checkout with unique unused path, e.g. `<primary-root>/.worktrees/login-<initials|bug-id>`.

Caveat: `feature/login` is already checked out at `/repo/.worktrees/login`. Git will refuse to check out the same branch twice. Either coordinate with the owner to reuse that checkout, or create a different branch from the same base commit in your new worktree. Never use `-B` / force to override checkout protection.

What worktrees share vs. isolate:

* Separate: working files, `HEAD`, index/staging area.
* Shared: objects, most refs/branches, remotes, much Git config. No security boundary.
* Per-worktree refs: `HEAD`, `refs/bisect/*`, `refs/worktree/*`, `refs/rewritten/*`. Coordinate shared ref mutations.
* Services may still collide: use distinct ports, DBs, output paths.

