Before offline — lock it. While offline — do not prune:

1. Confirm registration:
```sh
git -C "<repo>" worktree list --porcelain -z
```

2. Lock before unmount, with reason:
```sh
git -C "<repo>" worktree lock "<worktree>" --reason "share offline next week, task still active - do not prune"
```

3. Verify locked:
```sh
git -C "<repo>" worktree list --verbose
```

Do not while unavailable:
```sh
git -C "<repo>" worktree prune --dry-run --verbose
git -C "<repo>" worktree prune --verbose
git -C "<repo>" worktree unlock "<worktree>"
```

Missing directory = possible offline volume, not proof of removal. `lock` blocks `prune` and automatic `git gc` expiry via `gc.worktreePruneExpire`. Unlock only after share is back and path verified.

