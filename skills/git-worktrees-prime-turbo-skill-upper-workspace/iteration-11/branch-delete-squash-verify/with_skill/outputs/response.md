No — don't run `-D` yet. `git branch -d task/export` refusing after a squash-merge is expected: squash creates a new commit with no ancestry to `task/export`, so `-d` can't prove containment. `-d` also checks upstream, not your intended target — neither success nor failure is integration evidence.

Run in order, no filesystem deletion:

1. Confirm target + ownership + unused:
```bash
git worktree list
git branch -vv
git status
```
Require: branch is task-owned, not checked out in any worktree, no pending review. Closed PR is not sufficient.

2. Refresh and pin integration ref:
```bash
git fetch origin
git rev-parse --verify refs/heads/task/export refs/heads/main refs/remotes/origin/main
git log --oneline --first-parent -10 main
```
Identify the squash commit `<squash-sha>` on `main`.

3. Verify content, not ancestry:
```bash
git cherry main task/export
git log --cherry-pick --oneline --left-right main...task/export
git diff main task/export --stat
git diff $(git merge-base main task/export) task/export --stat
git show --stat <squash-sha>
```
Require: `cherry` shows all `-` / no `+`, endpoint `diff main task/export` is empty or only post-merge `main` work, and task-tip diff matches `<squash-sha>` diff. If `main` diverged, compare patches, not just empty diff.

4. Only then force-delete is acceptable — when work is verified integrated into `main`, preserved under another durable ref, or explicitly authorized to abandon obsolete history:
```bash
git branch -D task/export
git branch --list 'task/export'
git worktree list
```

5. Checkout removal leaves the branch; branch delete does not prune worktree metadata. Separately if you removed the checkout:
```bash
git worktree prune --dry-run
git worktree prune
```
Prune only if dry-run entries are intentionally removed checkouts.

