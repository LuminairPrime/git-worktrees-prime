Do not prune while unavailable - missing = offline volume, not stale.

Before offline, in order from `<primary-root>`:

1. Confirm registration and absolute path:
```sh
git -C "<repo>" worktree list --porcelain -v
```
Verify `<worktree>` is listed at its canonical absolute path.

2. Lock it to block `gc.worktreePruneExpire` / `prune --expire`:
```sh
git -C "<repo>" worktree lock --reason "share offline next week - task still active" "<worktree>"
```

3. Verify lock held:
```sh
git -C "<repo>" worktree list --porcelain -v
```
Require `locked` + reason on `<worktree>`.

4. Check auto-prune risk:
```sh
git config --get gc.worktreePruneExpire
```

While unmounted / unavailable, do not run:
```sh
git worktree prune
git worktree prune --dry-run -v
git gc
git -C "<repo>" worktree unlock "<worktree>"
git -C "<repo>" worktree remove "<worktree>"
```

After return: verify mount, `repair` if path changed, read lock reason from list output, then only `unlock`.

