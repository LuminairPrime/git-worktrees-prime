No.

All three bypass safeguards:

* `git worktree add -B`: resets the named branch to the selected commit. Only allowed when resetting is explicitly authorized; otherwise use `-b` for creation. Never override checkout protection.
* `rm -rf` on worktree directory: prohibited. Use `git worktree remove "<worktree>"` after the cleanup decision tree — verify owner, canonical path from `git worktree list --porcelain -z`, active use, tracked/untracked/ignored files, detached commits, and submodules.
* `prune` without dry-run / "prune everything": prohibited. Run `git worktree prune --dry-run --verbose` first, then prune only if every entry is an intentionally removed worktree. A missing directory may be an offline volume.

Safe alternative: list, inspect status, create with `-b` or reuse, remove via manager, then dry-run + prune with same expiry.
