Before offline, lock the registration so `gc`/`prune --expire` cannot drop it:

1. Check registration:
```sh
git worktree list -v
git worktree list --porcelain
```

2. Lock it:
```sh
git worktree lock "/mnt/share/<task>" --reason "share offline next week - task still active - do not prune"
```

3. Verify locked:
```sh
git worktree list -v
```

4. Record state before unmount:
```sh
git -C "/mnt/share/<task>" status -sb
git -C "/mnt/share/<task>" rev-parse HEAD
git -C "/mnt/share/<task>" branch --show-current
```

While unavailable, do not prune:

* No: do not run `git worktree prune`, `git worktree remove`, `git worktree repair`, or `git gc --prune=...`.
* A missing unlocked entry is prune-eligible. A locked entry is exempt and cheap to keep. Pruning would orphan the branch/worktree metadata.

After remount, validate then unlock:
```sh
git worktree list -v
git -C "/mnt/share/<task>" status -sb
git worktree unlock "/mnt/share/<task>"
```
