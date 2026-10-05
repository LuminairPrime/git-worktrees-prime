Would run in order, no deletion of `task/completed`:

1. Establish context:
```bash
pwd
git rev-parse --show-toplevel
git rev-parse --git-common-dir
git worktree list -v
git branch -vv
git status --short --branch
```

2. Verify squash-integration, do not use `--merged` - squash does not count as merged:
```bash
git fetch origin release task/completed
git log --oneline --graph --boundary release...task/completed
git cherry release task/completed
git diff release...task/completed --stat
git diff release...task/completed
```
Check: `cherry`/`diff` empty = content already in `release`. Keep branch because review is still open on `task/completed`.

3. Inventory completed checkout:
```bash
git -C case02/checkouts/completed status --short --branch
git -C case02/checkouts/completed status --short --ignored | head -n 50
git check-ignore -v case02/checkouts/completed/review.db
ls -lh case02/checkouts/completed/review.db
sha256sum case02/checkouts/completed/review.db
```

4. Preserve what review needs before reclaim:
```bash
cp -p case02/checkouts/completed/review.db ./review.db.task-completed-preserved
sha256sum ./review.db.task-completed-preserved
ls -lh ./review.db.task-completed-preserved
```
Check: hashes match step 3.

5. Protect unmounted colleague-owned checkout - get exact path from step 1 as `<offline-path>`:
```bash
git worktree lock <offline-path> --reason "colleague-owned offline-worker on unmounted share, still in use - do not prune"
git worktree list -v
```

6. Preview stale metadata:
```bash
git worktree prune --dry-run -v
```
Check: must list only retired `scratch` worktree, must NOT list `<offline-path>` due to lock, must NOT list `case02/checkouts/completed` - still on disk.

7. Reclaim completed checkout - requires `--force` due to ignored `review.db`:
```bash
git worktree remove --force case02/checkouts/completed
git worktree list -v
test ! -e case02/checkouts/completed && echo "completed removed"
test -f ./review.db.task-completed-preserved && sha256sum ./review.db.task-completed-preserved
```

8. Prune only the already-deleted-from-disk scratch entry:
```bash
git worktree prune -v
git worktree list -v
```

9. Final verification - appropriate local cleanup only:
```bash
git worktree list -v
git branch -vv
git branch --list task/completed
git status --short --branch
ls -lh ./review.db.task-completed-preserved
```

What remains precisely:
- `case02/checkouts/completed` path gone, `.git/worktrees/<completed>` admin gone.
- `task/completed` branch kept, `release` unchanged.
- `review.db` kept as `./review.db.task-completed-preserved` with matching hash.
- offline-worker entry kept, `locked`, path still registered but unmounted.
- retired `scratch` entry gone, pruned.
- No other branches/worktrees deleted.

