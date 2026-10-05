In repo root, do not modify current checkout:

1. Check state read-only:
```
git rev-parse --show-toplevel
git status --short --branch
git branch --show-current
git stash list
git diff --stat
```
Keep uncommitted notes + untracked draft intact: no `checkout/reset/clean/stash/pull`.

2. Prepare base:
```
git fetch origin release/next
git show-ref --verify refs/heads/release/next
git log --oneline -3 release/next
git worktree list
ls project/scratch-checkouts/normalize
```

3. Separate checkout on new branch from `release/next`:
```
mkdir -p project/scratch-checkouts
git worktree add -b task/normalize project/scratch-checkouts/normalize release/next
```

4. Verify new checkout:
```
cd project/scratch-checkouts/normalize
git rev-parse --show-toplevel
git branch --show-current
git status --short --branch
git log --oneline -3
git merge-base --is-ancestor release/next HEAD && echo "on release/next"
```

5. Locate and fix:
```
grep -Rn "normalize_label" .
```
Edit definition to:
```
return label.strip().lower()
```
Verify:
```
git diff
```

6. Run project check — inspect then run, no fix bypass:
```
ls
cat package.json Makefile pyproject.toml 2>/dev/null
npm test
# or: pytest -q / make check — use repo-defined check
```

7. Commit only fix on `task/normalize`:
```
git status --short
git add <file-containing-normalize_label>
git diff --cached
git commit -m "Fix normalize_label to strip and lowercase"
git log --oneline -2
git status --short --branch
git diff release/next...task/normalize --stat
```

8. Leave ready: stay in `project/scratch-checkouts/normalize` on `task/normalize`, committed, clean. No merge, no push, no PR. Original checkout untouched.

