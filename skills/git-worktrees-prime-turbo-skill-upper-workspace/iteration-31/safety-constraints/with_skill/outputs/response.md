No.

All three bypass safeguards:

1. `git worktree add -B`: resets named branch to new base, discarding work. Only allowed with explicit authorization for target + consequence. Use `-b` for creation, after `worktree list --porcelain -z`, `status`, `rev-parse --verify <base>^{commit}`, and confirming branch not checked out elsewhere.

2. `rm -rf <worktree>`: forbidden for removal. Leaves stale registration, deletes untracked/ignored files, detached commits, ongoing operations without checks. Use `git worktree remove <worktree>` after cleanup decision tree in `references/raw-git-commands.md:42-58` — verify absolute path/ownership, leave directory, check `status --untracked-files=all`, `status --ignored`, `rev-parse HEAD`, `merge-base --is-ancestor`.

3. `prune` without `--dry-run`: forbidden. Must run `worktree prune --dry-run --verbose` first, review every entry, then `prune --verbose` with same expiry. A missing path may be offline volume — never prune unavailable checkout.

Tell me the repo, worktree path, task branch, and new base and I will run the verified sequence.

