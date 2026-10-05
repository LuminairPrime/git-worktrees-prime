Do not prune while unavailable. Missing = possibly offline volume, not stale.

Before storage goes offline, lock it to block `gc.worktreePruneExpire`:

1. Confirm canonical path/registration:
```sh
git -C "<repo>" worktree list --porcelain -z
```
2. Lock with reason — flag precedes path:
```sh
git -C "<repo>" worktree lock --reason "<why-offline>" "<worktree>"
```

While unmounted, do not run:
```sh
git -C "<repo>" worktree prune --dry-run --verbose
git -C "<repo>" worktree prune --verbose
git -C "<repo>" worktree unlock "<worktree>"
```
Do not prune, unlock, move, delete, or recreate the live checkout to fix registration.

After storage returns, verify before other work:
```sh
git -C "<repo>" worktree list --porcelain -z
```
Only unlock after reading the lock reason, and if mount shift changed the path, repair first:
```sh
git -C "<repo>" worktree repair "<worktree>"
git -C "<repo>" worktree list --porcelain -z
```
