Before offline, `lock` the registration. While offline, do not `prune`.

In order, from main checkout:

1. Confirm registration:
```bash
git worktree list -v
git worktree list --porcelain
```

2. Check auto-expiry for `git gc`:
```bash
git config --get gc.worktreePruneExpire
```
Default if unset: `3.months.ago`. `git gc` prunes missing worktrees older than this.

3. Lock before unmount:
```bash
git worktree lock "/share/path/to/worktree" --reason "share offline next week, task still active"
```

4. Verify `locked`:
```bash
git worktree list -v
git worktree list --porcelain
cat "$(git rev-parse --git-common-dir)/worktrees/<name>/locked"
```

5. While unmounted, do not run:
```bash
git worktree prune
git worktree prune --expire now
git gc --prune=now
git worktree remove "/share/path/to/worktree"
```
This would delete `$(git-common-dir)/worktrees/<name>/` registration. When the share returns the worktree's `.git` file would point at missing admin data.

`locked` prevents `git gc` / `git worktree prune` from dropping it while missing.

After remount: `git worktree list -v`, confirm accessible, then `git worktree unlock "/share/path/to/worktree"`.

