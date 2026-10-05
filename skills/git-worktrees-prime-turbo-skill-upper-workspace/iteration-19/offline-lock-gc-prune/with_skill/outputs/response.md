Before the share goes offline, lock the registration. While it is unmounted, do not prune or unlock it.

In order, from a surviving checkout:

1. Confirm current registration:
```sh
git -C "<repo>" worktree list --porcelain -z
```
Verify the exact absolute `<worktree>` path is present.

2. Lock it before unmount:
```sh
git -C "<repo>" worktree lock "<worktree>" --reason "share offline, task still active"
```

3. Verify locked:
```sh
git -C "<repo>" worktree list --porcelain -z
```

This prevents `git gc` automatic expiry via `gc.worktreePruneExpire` from dropping the missing-path registration.

While unavailable, do not run:
```sh
git -C "<repo>" worktree prune --dry-run --verbose
git -C "<repo>" worktree prune --verbose
```

Reason: a missing directory may be an offline volume, not an intentionally removed worktree. Pruning would remove live-checkout metadata; unlocking would re-expose it to `gc`.

