No.

All three bypass safeguards:

* `git worktree add -B`: resets the named branch. Don't use unless resetting that branch to that commit is explicitly authorized. Use `-b` for creation. Must first verify base, branch ownership, and that branch is not checked out elsewhere.
* `rm -rf <worktree>`: don't delete worktrees via filesystem. Use manager or `git worktree remove "<worktree>"` after cleanup checks: still in use, still needed, tracked/untracked/ignored files, detached commits, unfinished operations, submodules, canonical path/ownership.
* `prune` without dry-run: don't. Required: `git worktree prune --dry-run --verbose`, review every entry, then `git worktree prune --verbose` with same expiry. A missing directory may be an offline volume — don't prune it as stale.

Being in a hurry is not authorization to discard work or bypass safeguards.

