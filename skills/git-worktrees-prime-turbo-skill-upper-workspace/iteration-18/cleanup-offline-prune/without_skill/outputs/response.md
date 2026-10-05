1. Inventory - do not modify yet:
```
git worktree list -v
git worktree list --porcelain
git branch -vv
git -C case02/checkouts/completed status --short --ignored
git -C case02/checkouts/completed check-ignore -v review.db
ls -lh case02/checkouts/completed/review.db
```
Identify from `list`: `<offline-path>` on unmounted share, `<scratch-path>` missing from disk.

2. Protect in-use missing worktree from prune:
```
git worktree lock "<offline-path>" --reason "colleague-owned, share currently unmounted, still in use - do not prune"
```

3. Preserve ignored file reviewer needs:
```
mkdir -p ./kept-for-review/
cp -a case02/checkouts/completed/review.db ./kept-for-review/review.db
ls -lh ./kept-for-review/review.db
test -f ./kept-for-review/review.db
```

4. Verify squash-integration before reclaim, do not delete branch:
```
git log --oneline -5 release
git diff release...task/completed --stat
git cherry release task/completed
```
Expected: empty diff/cherry - content in `release`. Keep `task/completed` because review open: no `git branch -d/-D task/completed`.

5. Reclaim only `completed`:
```
git worktree remove --force case02/checkouts/completed
```

6. Cleanup only stale admin data, offline protected by lock:
```
git worktree prune -n -v
git worktree prune -v
```

7. Final verification:
```
git worktree list -v
git worktree list --porcelain
git branch --list "task/completed" "release"
test -f ./kept-for-review/review.db && ls -lh ./kept-for-review/review.db
test ! -e case02/checkouts/completed
```

Report what remains:
- worktrees: main + `<offline-path>` locked, `case02/checkouts/completed` gone, `<scratch-path>` pruned.
- branches: `task/completed` kept for open review, `release` contains squash.
- file: `review.db` preserved at `./kept-for-review/review.db`.
- untouched: `<offline-path>` share, no force prune without lock.

