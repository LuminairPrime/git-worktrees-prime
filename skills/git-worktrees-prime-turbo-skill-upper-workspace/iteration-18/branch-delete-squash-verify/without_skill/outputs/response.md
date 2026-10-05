No — `git branch -d` refusing is expected after a squash-merge. Don't bypass it with `-D` until verified.

Why: squash creates a new commit on `main`, so `task/export` is not an ancestor of `main`. `git branch -d` only allows ancestry merges, so it correctly warns.

Run in order:

1. Update and confirm `main` has the squash:
```bash
git fetch origin
git checkout main
git pull --ff-only
git log --oneline -10
```

2. Confirm worktree is clean:
```bash
git worktree list
git status --short --branch
```

3. Check patch-equivalence — all lines must be `-`, none `+`:
```bash
git cherry main task/export
```
`+` = not in `main`, `-` = already applied via squash.

4. Check no content difference remains:
```bash
git diff main task/export --stat
git diff main task/export
```
Expect empty output. If non-empty, stop — inspect with:
```bash
git log --oneline --cherry-mark main...task/export
```

5. Check remote/PR state:
```bash
git branch -a | grep task/export
gh pr view task/export --json state,mergeCommit,mergedAt
```

`-D` is acceptable only when: `1-2` show `main` contains the squash commit, `3` is all `-`, `4` is empty, and `5` shows `MERGED` / no unique local work.

Then, optional backup and delete:
```bash
git tag archive/task/export task/export
git branch -D task/export
git push origin --delete task/export
git worktree prune
```

