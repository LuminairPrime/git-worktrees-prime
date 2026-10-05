1. Locate repo, no mutations:
```bash
pwd
git rev-parse --show-toplevel
git status --short --branch
git worktree list -v
git worktree list --porcelain -v
git branch -vv
```

Check: identify `case02/checkouts/completed [task/completed]`, offline-worker path on unmounted share, retired scratch path missing from disk.

2. Confirm squash-integration, open review must be kept:
```bash
git log --oneline -5 release
git log --oneline -5 task/completed
git cherry release task/completed
git branch --list task/completed -vv
```
Check: `git cherry` empty = content integrated. Do NOT run `git branch -d/-D task/completed` - review remains open on it.

3. Confirm completed worktree state + ignored file needing preservation:
```bash
git -C case02/checkouts/completed status --short --branch --ignored
git check-ignore -v case02/checkouts/completed/review.db
ls -lh case02/checkouts/completed/review.db
sha256sum case02/checkouts/completed/review.db
```
Check: tracked tree clean, only `review.db` ignored present.

4. Preserve `review.db` outside worktree before reclaim:
```bash
mkdir -p ./saved-review
cp -p case02/checkouts/completed/review.db ./saved-review/review.db
sha256sum ./saved-review/review.db
ls -lh ./saved-review/review.db
```
Check: checksums match.

5. Protect in-use but currently unmounted offline-worker from prune. Using `<offline-path>` from step 1:
```bash
test -e <offline-path> || echo "unmounted/missing as expected - do not touch"
git worktree lock <offline-path> --reason "colleague-owned, still in use, share currently unmounted"
git worktree list --porcelain -v
```
Check: offline entry shows `locked`.

6. Reclaim completed checkout:
```bash
git worktree remove -v case02/checkouts/completed
```
Only if it fails for squash-dirty-lock reason after step 3 proved clean/integrated, then:
```bash
git -C case02/checkouts/completed status --short
git worktree remove --force -v case02/checkouts/completed
```
Check:
```bash
test ! -e case02/checkouts/completed && echo "reclaimed"
git worktree list -v
```

7. Cleanup only dead retired scratch entry, spare locked entry:
```bash
git worktree prune -v --dry-run
git worktree prune -v
git worktree list --porcelain -v
```
Check: dry-run must list only `<retired-scratch-path>`, NOT locked `<offline-path>`. After prune, scratch admin entry gone.

8. Final report - what remains:
```bash
git worktree list -v
git worktree list --porcelain -v
git branch -vv
git branch --list task/completed -vv
ls -lh ./saved-review/review.db
sha256sum ./saved-review/review.db
git worktree prune -v --dry-run
```
Report: main worktree + locked offline-worker worktree remain, `case02/checkouts/completed` gone/reclaimed, retired scratch pruned, `task/completed` branch kept, `review.db` kept only at `./saved-review/review.db`.

