1. Inventory - do not change anything:
```bash
git worktree list --verbose
git worktree list --porcelain
git branch -vv
git status --porcelain=v1 --branch
ls .git/worktrees/
for d in .git/worktrees/*; do echo "== $d"; cat "$d/gitdir"; cat "$d/locked" 2>/dev/null || echo "not-locked"; done
```

2. Check `completed` checkout state:
```bash
git -C case02/checkouts/completed status --porcelain=v1 --branch --ignored
git -C case02/checkouts/completed log --oneline -5
ls -lh case02/checkouts/completed/review.db
git -C case02/checkouts/completed check-ignore -v review.db
sha256sum case02/checkouts/completed/review.db
```

3. Verify squash-integration, keep branch:
```bash
git show-ref --verify refs/heads/task/completed
git show-ref --verify refs/heads/release
git log --oneline --graph release -5
git diff --stat release...task/completed
git cherry release task/completed
```
Check: `diff release...task/completed` empty/no unique content, `release` contains squash commit. Do NOT delete `task/completed` - review open.

4. Preserve what review needs - ignored file is deleted with worktree:
```bash
mkdir -p ./kept-for-review
cp -p case02/checkouts/completed/review.db ./kept-for-review/review.db
ls -lh ./kept-for-review/review.db
sha256sum ./kept-for-review/review.db
```

5. Reclaim only `completed` checkout, keep branch:
```bash
git worktree remove case02/checkouts/completed
# use --force only if blocked by non-ignored untracked/modified files after inspection in step 2
test -d case02/checkouts/completed && echo "still-exists" || echo "reclaimed"
git worktree list --verbose
git show-ref --verify refs/heads/task/completed
```

6. Stale entries - do NOT run bare `git worktree prune`:
```bash
git worktree prune -n -v
```
Dry-run will list both `offline-worker/unmounted-share` and `retired-scratch/deleted` as prunable. Prune only deleted one:
```bash
rm -rf .git/worktrees/<retired-scratch-admin-dir-name>
git worktree lock --reason "colleague-owned still in use on currently unmounted share - do not prune" -- <offline-worker-path>
git worktree list --verbose
git worktree prune -n -v
```

7. Final verification:
```bash
git worktree list --verbose
git branch --list "task/completed" -vv
git status --porcelain=v1 --branch
ls -lh ./kept-for-review/review.db
sha256sum ./kept-for-review/review.db
```

What remains:
* `case02/checkouts/completed/` removed, worktree unregistered.
* `refs/heads/task/completed` retained, unchanged - open review.
* `release` unchanged, contains squash-integration.
* `./kept-for-review/review.db` preserved, verified by `sha256sum`.
* offline-worker worktree registration retained + `locked`, still points to unmounted colleague-owned share, not pruned.
* retired scratch worktree admin dir removed, no worktree entry.

