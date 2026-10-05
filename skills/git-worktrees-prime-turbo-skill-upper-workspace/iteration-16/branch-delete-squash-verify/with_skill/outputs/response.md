No. Do not run `git branch -D task/export` yet. `-d` refusing is expected after squash-merge.

`branch -d` checks ancestry, not content. Squash creates a new commit, so:

```sh
git merge-base --is-ancestor task/export main
```

will fail exit `1` even when fully integrated.

Run in order from a surviving checkout:

1. Refresh integration ref:
```sh
git fetch origin
git rev-parse --verify "refs/heads/task/export^{commit}"
git rev-parse --verify "refs/heads/main^{commit}"
git worktree list --porcelain -z
```

2. Ancestry check - document expected failure:
```sh
git merge-base --is-ancestor task/export main; echo $?
```

3. Verify replacement integration:
```sh
git log --oneline -5 main
git diff main...task/export
git cherry main task/export
```
Require: `diff` empty, `cherry` shows only `-` lines. That proves all unique `task/export` changes exist in `main` under the squash commit. A closed PR alone is insufficient.

4. Ownership/retention check: task-owned, not checked out elsewhere, no pending review needing the branch, or explicit abandonment authorized.

Only then `-D` is acceptable:
```sh
git branch -D task/export
git branch --list "task/export"
git worktree list --porcelain -z
```

