Before offline — `lock` it, so `gc` cannot expire it:

1. Confirm canonical path + registration:
```sh
git -C "<repo>" worktree list --porcelain -z
```
2. Check auto-expire that `git gc` will use:
```sh
git -C "<repo>" config --get gc.worktreePruneExpire
```
3. Lock the live checkout before unmount:
```sh
git -C "<repo>" worktree lock --reason "share offline next week, task still active" "<worktree>"
```
4. Verify `locked`:
```sh
git -C "<repo>" worktree list --verbose
```

While unavailable — do not prune or unlock:

* No: missing directory may be offline volume, not a removed worktree.
* Do not run:
```sh
git -C "<repo>" worktree prune --dry-run --verbose
git -C "<repo>" worktree prune --verbose
git -C "<repo>" worktree unlock "<worktree>"
```
Unlock/repair only after the share is remounted and `worktree list` verifies the path again.

