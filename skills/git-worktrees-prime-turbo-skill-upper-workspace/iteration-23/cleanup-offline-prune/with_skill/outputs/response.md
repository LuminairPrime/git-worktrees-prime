Reclaim `case02/checkouts/completed`, retain `task/completed` for open review:

1. Locate primary, confirm registrations:
```bash
pwd
git rev-parse --show-toplevel
git worktree list -v
git worktree list --porcelain -z
```
Check: `case02/checkouts/completed` registered to `task/completed`, offline-worker path registered but unmounted/colleague-owned, retired scratch path registered but deleted.

2. Verify branch / integration target, squash breaks ancestry:
```bash
git fetch origin
git rev-parse --verify refs/heads/task/completed
git rev-parse --verify refs/heads/release
git log --oneline -5 task/completed
git log --oneline -5 release
git diff release...task/completed --stat
git diff release task/completed --stat
```
Check: functional diff empty/in release, `task/completed` not ancestry-merged. `branch -d` refusal expected, retain branch.

3. Inspect disappearing state in completed checkout:
```bash
git -C case02/checkouts/completed rev-parse --abbrev-ref HEAD
git -C case02/checkouts/completed status --porcelain=v1 -uall
git -C case02/checkouts/completed status --porcelain=v1 --ignored -uall
git -C case02/checkouts/completed ls-files --others --ignored --exclude-standard
ls -l case02/checkouts/completed/review.db
sha256sum case02/checkouts/completed/review.db
git -C case02/checkouts/completed stash list
```
Check unfinished ops, detached commits, submodules separately. Confirm only valuable unrecoverable state is ignored `review.db`.

4. Preserve outside deletion path:
```bash
mkdir -p /tmp/opencode/preserve-task-completed
cp -a case02/checkouts/completed/review.db /tmp/opencode/preserve-task-completed/review-task-completed.db
sha256sum /tmp/opencode/preserve-task-completed/review-task-completed.db
ls -l /tmp/opencode/preserve-task-completed/
```
Check checksums match.

5. Leave checkout before removal:
```bash
cd "$(git rev-parse --show-toplevel)"
pwd
```

6. Remove only exact checkout, no force, no `rm -rf`:
```bash
git worktree remove "case02/checkouts/completed"
```
Do not use `--force`.

7. Retain branch for review, do not delete:
```bash
git branch --list "task/completed"
git rev-parse --verify refs/heads/task/completed
```
Do not run `git branch -d/-D task/completed`.

8. Stale metadata check, do not harm offline volume:
```bash
git worktree prune --dry-run -v
```
Check: dry-run lists scratch + offline-worker missing/unmounted. Since not every entry is intentionally removed, do not run `git worktree prune -v`, do not `unlock/move` offline-worker.

9. Verify result:
```bash
git worktree list -v
git worktree list --porcelain -z
test ! -e case02/checkouts/completed && echo "completed removed"
git branch --list "task/completed"
ls -l /tmp/opencode/preserve-task-completed/review-task-completed.db
```

Remains:
- `refs/heads/task/completed` retained for open review.
- `/tmp/opencode/preserve-task-completed/review-task-completed.db` preserved copy of ignored `review.db`.
- offline-worker registration retained, unmounted, colleague-owned, still in use, not pruned/unlocked.
- retired scratch stale registration retained, not pruned to protect offline-worker.
- primary checkout untouched.

Removed:
- directory + registration `case02/checkouts/completed` only.

