In order, read-only first, never touch current checkout:

```bash
pwd
git rev-parse --show-toplevel
git status --short --branch
git ls-files --others --exclude-standard
git diff --stat
git branch --show-current
git branch -a --list *release/next* *task/normalize*
git rev-parse --verify release/next
git worktree list
```

Sync base without touching worktree:
```bash
git fetch origin release/next --prune --no-tags
git rev-parse --verify release/next
git log --oneline -3 release/next
```

Create separate checkout on new branch from `release/next`:
```bash
git worktree add -b task/normalize project/scratch-checkouts/normalize release/next
```

Verify new checkout clean and based correctly:
```bash
cd project/scratch-checkouts/normalize
git rev-parse --show-toplevel
git branch --show-current
git status --short --branch
git log --oneline -3
git merge-base --is-ancestor release/next HEAD && echo "based on release/next"
```

Locate and fix, read-only inspect first:
```bash
grep -rn "normalize_label" .
# read returned file, then edit only that file to:
# return label.strip().lower()
git diff
git diff --check
```

Discover and run project's documented check in new checkout only:
```bash
ls -a
cat package.json Makefile pyproject.toml tox.ini 2>/dev/null | head -n 100
# run what repo documents, e.g.:
pytest -q
```

Commit fix on task branch, specific file only:
```bash
git status --short
git add <path/to/file/with/normalize_label>
git diff --cached
git diff --cached --check
git commit -m "fix: strip whitespace and lowercase in normalize_label"
git log --oneline -3
git status --short --branch
git worktree list
```

Leave for review, verify original intact, do not publish:
```bash
cd ../../..
git status --short --branch
git ls-files --others --exclude-standard
# STOP: do not run git merge, git switch in project/, git stash, git clean/reset, git push, gh pr create
```

