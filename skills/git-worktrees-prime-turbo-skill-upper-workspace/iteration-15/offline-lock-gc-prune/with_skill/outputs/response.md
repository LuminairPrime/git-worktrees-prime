Before offline — lock it, do not prune after:

1. Confirm registration and canonical path:
```sh
git -C "<repo>" worktree list --porcelain -z
```

2. Lock before share goes offline — prevents `git gc` / `gc.worktreePruneExpire` auto-prune:
```sh
git -C "<repo>" worktree lock --reason "share offline, task still active" "<worktree>"
```

3. Verify locked:
```sh
git -C "<repo>" worktree list --porcelain -z
```

While unavailable — do not prune:

* Do NOT run:
```sh
git -C "<repo>" worktree prune --dry-run --verbose
git -C "<repo>" worktree prune --verbose
```
* Do NOT `worktree unlock`, do NOT force-expire with `gc` / `gc.worktreePruneExpire`.

Missing = offline volume, not stale. Prune only intentionally-removed worktrees where every dry-run entry was reviewed.

