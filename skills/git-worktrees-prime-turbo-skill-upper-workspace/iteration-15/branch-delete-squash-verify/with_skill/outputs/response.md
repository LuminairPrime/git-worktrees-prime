No — do not run `git branch -D task/export` yet. `git branch -d` refusal is expected after squash-merge: ancestry is broken, so `task/export` looks unmerged even if content is integrated. `-d` also checks upstream, not `main`.

Verify integration first, in order:

1. Confirm state, not in task branch/checkout:
```bash
git worktree list
git branch --show-current
git branch --list "task/export"
git status --short --branch
```

2. Get current integration ref:
```bash
git fetch origin
git log --oneline -15 origin/main
```

3. Check patch-equivalence, not ancestry. All lines must be `-`, empty is fully integrated:
```bash
git cherry origin/main task/export
git log --cherry-pick --oneline --left-right origin/main...task/export
```

If any `+` remains: not fully integrated — stop, inspect that commit with `git show <sha>` / `git diff`.

4. Confirm resulting file changes match squash commit:
```bash
git diff origin/main...task/export --stat
git diff origin/main...task/export
```
Must be empty or only changes intentionally kept/discarded in squash review. A closed PR alone is insufficient.

5. If `worktree list` still shows stale registration for removed checkout:
```bash
git worktree prune -n -v
git worktree prune
git worktree list
```

`-D` is acceptable only when: `cherry` shows no `+`, `diff` shows no unintegrated work, branch is task-owned/unneeded for pending review, and discarding its obsolete history is authorized.

Then:
```bash
git branch -D task/export
git branch --list "task/export"
```
Delete `origin/task/export` with `git push origin --delete` only if separately in scope.
