Reclaim `case02/checkouts/completed`, retain `task/completed` for open review:

1. Inventory, do not `cd` into target:
```bash
pwd
git rev-parse --show-toplevel
git worktree list -v
git worktree list --porcelain -z
```

2. Confirm target checkout identity/owner/state:
```bash
git -C case02/checkouts/completed rev-parse --abbrev-ref HEAD
git -C case02/checkouts/completed rev-parse HEAD
git -C case02/checkouts/completed log --oneline -3
git -C case02/checkouts/completed status
git -C case02/checkouts/completed status --porcelain=v1 -uall --ignored
git -C case02/checkouts/completed submodule status
```

3. Verify squash-integration vs current `release`, retain branch for review:
```bash
git fetch origin release
git rev-parse --verify release
git rev-parse --verify task/completed
git log --oneline -5 release
git diff release...task/completed --stat
git cherry release task/completed
```
Check: tip preserved on `task/completed`, review still open -> do NOT run `git branch -d/-D task/completed`.

4. Confirm and preserve ignored state outside deletion path:
```bash
git -C case02/checkouts/completed check-ignore -v review.db
ls -lh case02/checkouts/completed/review.db
cp -a case02/checkouts/completed/review.db <preserved-path-outside-worktree>/review.db
ls -lh <preserved-path-outside-worktree>/review.db
sha256sum case02/checkouts/completed/review.db <preserved-path-outside-worktree>/review.db
```

5. Leave directory, remove only exact checkout via Git:
```bash
cd "$(git rev-parse --show-toplevel)"
git worktree remove case02/checkouts/completed
```
No `--force`, no `rm -rf`, no `move`.

6. Verify removal:
```bash
test ! -e case02/checkouts/completed && echo "removed"
git worktree list -v
git worktree list --porcelain -z
git branch --list task/completed
git rev-parse --verify task/completed
```

7. Stale registration dry-run, then abort prune:
```bash
git worktree prune -n -v
```
Check: lists retired `scratch` missing-from-disk + `offline-worker` missing-due-to-unmounted-share. Per rule: missing may be offline volume, prune only if every entry intentionally removed. Result contains colleague-owned still-in-use `offline-worker` -> do NOT run `git worktree prune -v`, do NOT unlock.

8. Final verification:
```bash
git worktree list -v
git branch --list task/completed
ls -lh <preserved-path-outside-worktree>/review.db
```

Remains:
- Removed: `case02/checkouts/completed` directory/registration.
- Retained: branch `task/completed` for open review, preserved `review.db` at `<preserved-path-outside-worktree>/review.db`.
- Retained: `offline-worker` registration - unmounted, colleague-owned, in use.
- Retained: retired `scratch` stale registration - deleted from disk but cannot safely prune while `offline-worker` entry present.

