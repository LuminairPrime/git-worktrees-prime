Before offline - lock it, do not prune it while missing:

1. Check registration and lock state:
```bash
git worktree list --verbose
```

2. Lock the offline-bound worktree:
```bash
git worktree lock "/path/to/task-worktree" --reason "share offline next week - task still active"
```

3. Verify `locked` appears:
```bash
git worktree list --verbose
```

`git gc` runs effectively `git worktree prune --expire <gc.worktreePruneExpire>` default `3.months.ago`. `lock` creates `.git/worktrees/<name>/locked` and exempts that registration from `prune`/`gc`.

While unavailable - answer is no, do not prune:

4. Do NOT run while unmounted:
```bash
git worktree prune
git worktree prune --expire=now
git gc --prune=now
git worktree remove --force "/path/to/task-worktree"
```

Missing != deleted. Pruning then deletes `.git/worktrees/<name>/` metadata and orphans the worktree.

After remount:

5. Verify back and unlock:
```bash
git worktree list --verbose
git worktree unlock "/path/to/task-worktree"
git worktree list --verbose
```

Only `prune` a worktree registration you know was intentionally deleted and will never return.

