Before offline, lock the registration. While unavailable, do not prune:

1. Confirm canonical path and current registration:
```sh
git -C "<repo>" worktree list --porcelain -z
```

2. Lock before share goes offline, task still active:
```sh
git -C "<repo>" worktree lock --reason "share offline next week - task still active" "<worktree>"
```

3. Verify locked registration:
```sh
git -C "<repo>" worktree list --porcelain -z
```

4. While unmounted/missing: do not prune or unlock:
```sh
git -C "<repo>" worktree prune --dry-run --verbose
git -C "<repo>" worktree prune --verbose
```
Do not run either. A missing directory may be an offline volume, not a stale intentionally-removed worktree. `git gc` can auto-prune missing registrations via `gc.worktreePruneExpire`; the lock preserves it.

