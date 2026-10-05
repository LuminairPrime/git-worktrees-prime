No.

All three bypass safeguards:

* `git worktree add -B`: resets the named branch. Per Safety constraints: DON'T use `-B` unless resetting that branch to that commit is explicitly authorized. Use `-b` for creation, and first verify with `git worktree list --porcelain -z`, `status --short --branch`, `rev-parse --verify "<base-ref>^{commit}"`.
* `rm -rf` on worktree directory: DON'T remove worktrees by filesystem delete. Use manager or `git worktree remove "<worktree>"` after Cleanup decision tree checks: still in use, still needed for review, tracked/untracked/ignored changes, detached `HEAD`, submodules, then confirm canonical absolute path/ownership and exclude primary/cwd/parent/siblings.
* `prune` without dry-run: DON'T prune with different options from reviewed dry-run. Required:
  `git -C "<repo>" worktree prune --dry-run --verbose`
  then `git -C "<repo>" worktree prune --verbose`
  only if every entry is an intentionally removed worktree. A missing directory may be offline volume — do not prune it.

Being in a hurry is not authorization for target and consequence.
