No. `git branch -d task/export` refusing is expected after a squash-merge.

`-d` checks ancestry: `task/export` tip is not an ancestor of `main`. Squash creates a new commit SHA, so ancestry is never preserved. `-D` bypasses that check and will lose unique commits if the squash was partial/stale.

Run in order:

1. Sync and locate integration:
```
git fetch origin
git checkout main
git pull --ff-only
git branch -vv
git branch --merged main
git branch --no-merged main
git log --oneline -10 main
git log --oneline main --grep="export" --grep="task/export"
git worktree list
```

2. List what `-D` would discard:
```
git log main..task/export --oneline
git cherry main task/export
```

`cherry` should show `-` for every commit = patch-equivalent to `main`. `+` means not upstream.

3. Verify content equality against the squash commit, not `main` tip:
```
git diff <squash-sha> task/export --stat
git diff <squash-sha> task/export --
```

Expect empty or only conflict-resolution noise. If `main` moved on, don't use `git diff main task/export`, use the squash SHA.

`-D` is acceptable only when:

* `main` is up to date with `origin/main`,
* PR is marked Merged,
* `cherry` is all `-` and diff in step 3 is clean,
* `main..task/export` contains nothing you need to keep.

Then:
```
git branch -D task/export
git push origin --delete task/export # only if remote branch exists
git fetch -p
git branch -a | grep task/export
```
