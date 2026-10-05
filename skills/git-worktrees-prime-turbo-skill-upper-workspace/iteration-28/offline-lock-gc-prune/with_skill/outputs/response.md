Before offline — lock it. While offline — do not prune/unlock:

1. Confirm registration from main/bare repo:
```sh
git -C "<repo>" worktree list --porcelain -z
```

2. Lock before unmount, reason flag precedes path:
```sh
git -C "<repo>" worktree lock --reason "<why-offline>" "<worktree>"
```
This prevents `git gc` auto-prune via `gc.worktreePruneExpire`.

3. While unavailable, do not run:
```sh
git -C "<repo>" worktree prune --dry-run --verbose
git -C "<repo>" worktree prune --verbose
git -C "<repo>" worktree unlock "<worktree>"
```
A missing directory may be an offline volume. Prune only if every dry-run entry is an intentionally removed worktree. Never prune or unlock a merely unavailable checkout.

After it returns: re-list, read lock reason, then `unlock` / `repair` only if path changed and checkout is live.

