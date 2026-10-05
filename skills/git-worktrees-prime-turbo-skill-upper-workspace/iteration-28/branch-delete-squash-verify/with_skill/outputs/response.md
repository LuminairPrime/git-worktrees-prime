No — do not run `git branch -D task/export` yet. `git branch -d` refusal is expected after squash-merge.

`-d` checks ancestry, not equivalence. Squash creates a new commit on `main`, so `task/export` is never an ancestor of `main`, even when fully integrated.

Verify integration first, in order:

1. Confirm checkout state, branch still exists:
```bash
git worktree list --porcelain
git branch -vv --list task/export
git branch -r --list 'origin/task/export'
```

2. Get current integration target:
```bash
git fetch origin
git rev-parse --verify refs/heads/main
git rev-parse --verify refs/remotes/origin/main
git rev-parse --verify refs/heads/task/export
```

3. Find the squash commit on `main`:
```bash
git log --oneline -10 origin/main
git log --oneline --grep='export' origin/main
```

4. Verify no unique changes remain on task branch:
```bash
git cherry origin/main task/export
git diff --stat origin/main...task/export
git log --cherry-mark --oneline origin/main...task/export
```
Integrated iff:
* `git cherry` shows only `-` lines, no `+` lines
* `git diff origin/main...task/export` is empty
* `git log --cherry-mark` shows only `=` / no `+` commits

A closed PR alone is insufficient — you need the above diff/cherry proof.

5. Check ownership / in-use:
* `git worktree list` must not show `task/export` checked out elsewhere
* `task/export` is task-owned, not needed for pending review, no detached commits worth keeping

Only then `-D` is acceptable:

```bash
git branch -D task/export
git push origin --delete task/export # if remote branch exists
git worktree prune -n
git worktree prune # only if dry-run entries are your intentionally removed checkout
git worktree list --porcelain
git branch --list 'task/export'
git fetch --prune origin
```

Summary: `-D` is for deleting a verified-obsolete, task-owned, unused branch whose changes are proven present in `origin/main` via `cherry` + three-dot `diff`.
