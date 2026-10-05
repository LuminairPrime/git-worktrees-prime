Would run in order, no deletion of `task/completed`:

1. Inventory:
```
git rev-parse --show-toplevel
git worktree list -v
git worktree list --porcelain
git branch -vv
git status -sb
```

2. Inspect `completed` checkout:
```
git -C case02/checkouts/completed rev-parse --abbrev-ref HEAD
git -C case02/checkouts/completed status -sb --ignored
git -C case02/checkouts/completed log --oneline -5
ls -lh case02/checkouts/completed/review.db
sha256sum case02/checkouts/completed/review.db
git check-ignore -v -- case02/checkouts/completed/review.db
```

3. Verify squash-integration, keep branch:
```
git fetch origin release task/completed
git log --oneline -5 release
git cherry release task/completed
git diff --stat release...task/completed
git branch -vv --list task/completed
```
Expected: `cherry` shows `-` lines / empty diff = applied, but do NOT `git branch -d/-D task/completed` - review still open.

4. Preserve ignored file outside worktree to be deleted:
```
cp -a case02/checkouts/completed/review.db ./review.db.task-completed.keep
ls -lh ./review.db.task-completed.keep
sha256sum ./review.db.task-completed.keep case02/checkouts/completed/review.db
```

5. Reclaim checkout:
```
git worktree remove --force case02/checkouts/completed
git worktree list -v
test ! -e case02/checkouts/completed && echo "removed"
```

6. Safe cleanup without touching unmounted colleague worktree:
```
git worktree prune -n -v
git worktree lock --reason "colleague-owned offline-worker on unmounted share, still in use - do not prune" <offline-worker-path-from-step-1>
git worktree prune -v
git worktree list -v
```

7. Report remainder:
```
git worktree list -v
git worktree list --porcelain
git branch -vv --list task/completed
git log --oneline -3 release
ls -lh ./review.db.task-completed.keep; sha256sum ./review.db.task-completed.keep
git status -sb
```

Remains: main worktree + locked offline-worker path (still listed, locked, not pruned); no entry for `case02/checkouts/completed` or retired scratch (pruned as missing); local/remote `task/completed` intact; `review.db` only at `./review.db.task-completed.keep` with matching hash.

