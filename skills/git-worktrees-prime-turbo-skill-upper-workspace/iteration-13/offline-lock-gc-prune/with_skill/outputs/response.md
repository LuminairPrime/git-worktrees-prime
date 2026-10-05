Before offline — lock it. While offline — do not prune:

1. Confirm registration and absolute path:
```sh
git -C "<primary-root>" worktree list --porcelain -z
```
Verify the share path is listed, owned by this task.

2. Lock before share goes offline:
```sh
git -C "<primary-root>" worktree lock "<worktree-abs-path>" --reason "share offline next week - task still active"
```

3. Verify lock:
```sh
git -C "<primary-root>" worktree list -v
```

4. While unmounted, do not prune/unlock:
```sh
# DO NOT RUN while unavailable:
git worktree prune
git worktree prune --expire
git gc
git worktree unlock "<worktree-abs-path>"
```

Reason: `git gc` auto-prunes missing registrations per `gc.worktreePruneExpire`. A locked registration is protected. A missing directory may be an offline volume — prune only intentionally-removed worktrees verified by dry-run, never just because path is unavailable.

