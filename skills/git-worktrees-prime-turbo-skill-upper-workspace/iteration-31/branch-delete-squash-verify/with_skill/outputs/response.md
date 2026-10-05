No — don't run `-D` yet. `git branch -d task/export` refusal is expected after squash-merge.

Why: squash creates a new commit on `main`, no ancestry link to `task/export`. `-d` checks ancestry/upstream, not content equivalence. Failure does not mean lost, success would not prove integration.

Run in order:

1. Confirm branch/checkout state:
```bash
git worktree list
git branch --list task/export
git rev-parse --verify refs/heads/task/export
git log --oneline -5 task/export
```

2. Refresh target:
```bash
git fetch origin
git rev-parse --verify refs/heads/main
git rev-parse --verify refs/remotes/origin/main
git log --oneline -5 main
git log --oneline -5 origin/main
```

3. Find squash commit:
```bash
git log --oneline --grep=export -10 main
git log --oneline --grep=#<PR-number> -10 main
```

4. Verify content integrated — need all `-`, no unique `+`:
```bash
git cherry main task/export
git cherry origin/main task/export
git diff origin/main task/export --stat
git diff main task/export --stat
```
Integrated if: `cherry` shows only `-` lines, and `diff` is empty or only post-squash `main` progress. If `main` advanced, restrict diff to touched files. Closed PR alone is insufficient.

5. Check remote / review retention:
```bash
git branch -vv | grep task/export
git branch -r --list origin/task/export
```
Retain if pending review needs it.

`-D` acceptable only when: 1) patch verified in current `main`/`origin/main` above, 2) branch is unused task-owned, no checkout owns it, 3) no review needs it, or abandonment explicitly authorized. Then:
```bash
git branch -D task/export
# remote only if separately in scope:
git push origin --delete task/export
```

