Before offline, `lock` it. While offline, do not `prune`:

1. Check registration:
```sh
git worktree list --verbose
```

2. Lock the share path:
```sh
git worktree lock "/path/to/task-worktree" --reason "share offline until DATE - do not prune"
```

3. Verify `locked`:
```sh
git worktree list --verbose
```

`lock` writes `<common-dir>/worktrees/<id>/locked` and exempts it from `git worktree prune` and `git gc`'s `gc.worktreePruneExpire` cleanup.

4. While unmounted, do not run:
```sh
git worktree prune
git gc --prune=now
```
That would delete the registration if it were not locked.

5. After remount:
```sh
git worktree unlock "/path/to/task-worktree"
git worktree list --verbose
git worktree prune -n --verbose
```
