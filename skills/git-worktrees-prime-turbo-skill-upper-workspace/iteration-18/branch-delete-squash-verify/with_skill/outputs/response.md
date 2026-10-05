No - do not run `git branch -D task/export` yet. For squash-merge `branch -d` refusal is expected: squash creates a new commit SHA with no ancestry to `task/export`, so Git correctly reports `not merged`.

Run in order from `<primary-root>`:

1. Confirm you are not on the branch and checkout is gone:
```bash
git worktree list --porcelain
git branch --show-current
git rev-parse --verify refs/heads/task/export
```

2. Get current integration ref:
```bash
git fetch origin main
git rev-parse main
git rev-parse origin/main
git rev-parse task/export
git log --oneline --decorate -10 main
git log --oneline --decorate -10 task/export
```
Identify the squash commit on `main`.

3. Verify patch-equivalence, `branch -d` / `--merged` cannot do this for squash:
```bash
git cherry main task/export
git diff main task/export --stat
git diff main task/export
```
Required result: `cherry` shows `-` for every task commit, and `diff` shows no unique `task/export` changes missing from `main`. Inspect any remaining diff - it must only be forward progress on `main`, not lost task work. A closed PR alone is insufficient.

4. Validate the integrated result on `main` - review/tests per repo workflow.

`-D` is acceptable only when all true:
* tip-to-`main` comparison above proves integration,
* branch is task-owned, not checked out elsewhere, not needed for pending review,
* obsolete pre-squash history is authorized to discard.

Then:
```bash
git branch -D task/export
git branch --list 'task/*'
git worktree list --porcelain
```

