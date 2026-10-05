No — don't run that as-is.

* `git worktree add -B` force-resets the branch — discards commits not on the new base.
* `rm -rf` on the worktree deletes uncommitted / untracked work permanently.
* `prune` without dry-run removes worktree metadata you can't verify afterward.

Safe order first:
1. `git status` + `git worktree list` to confirm clean state
2. Stash/commit or backup any work
3. `git worktree prune --dry-run`, then prune only if expected
