No.

All three shortcuts violate safety constraints:

1. `git worktree add -B`: resets the named branch to the new base, discarding its commits. Don't use `-B` unless that reset is explicitly authorized. Use `-b` for a new branch, or reuse the existing branch only after verifying it is not checked out elsewhere.

2. `rm -rf` on the worktree directory: don't delete worktrees via filesystem commands. This leaves stale registration and risks deleting uncommitted changes, untracked/ignored files, detached commits, or the wrong path. Use `git worktree remove "<worktree>"` after the cleanup checks: verify absolute path via `git worktree list --porcelain -z`, ownership, `status --short --branch --untracked-files=all`, `status --short --ignored`, `rev-parse HEAD`, and confirm no agent/editor/service still uses it.

3. `prune` without dry-run: don't. Run `git worktree prune --dry-run --verbose` first, review every entry — a missing directory may be an offline volume, not a deleted worktree. Only then run `git worktree prune --verbose` with the same expiry options.

Safe order: verify branch/tip and preservation, `worktree remove`, verify integration before any `branch -d`, then dry-run prune + prune.

