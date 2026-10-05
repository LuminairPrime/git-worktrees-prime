Exact sequence, in order, without touching current checkout state:

1. Record starting state - read only:
```sh
pwd
git rev-parse --show-toplevel
git branch --show-current
git status --short
git log --oneline -3 release/next
```

2. Update base ref only, do not checkout / stash / reset colleague work:
```sh
git fetch origin release/next
```

3. Create isolated checkout on new branch from `release/next`:
```sh
mkdir -p project/scratch-checkouts
git worktree add -b task/normalize project/scratch-checkouts/normalize release/next
```

4. Verify new checkout - must be clean, on task branch:
```sh
cd project/scratch-checkouts/normalize
git branch --show-current
git log --oneline -3
git status --short
git worktree list
```

5. Locate target:
```sh
grep -rn "normalize_label" .
```

6. Read the file containing `def normalize_label`, then fix to:
```python
return label.strip().lower()
```
Verify no other logic changed.

7. Smoke-check fix:
```sh
python3 -c "from <module> import normalize_label; assert normalize_label('  Hello ')=='hello', normalize_label('  Hello ')"
```

8. Discover and run project check - read only first:
```sh
ls
cat package.json Makefile pyproject.toml tox.ini 2>/dev/null
```
Then run what the repo defines, e.g. one of:
```sh
pytest -q
npm test
make check
```

9. Commit on task branch only:
```sh
git diff
git add <path-to-file-with-normalize_label>
git status --short
git commit -m "Fix normalize_label to strip whitespace and lowercase"
```

10. Leave ready for review, no merge/publish:
```sh
git branch --show-current
git log --oneline -2
git status --short
git diff release/next...HEAD --stat
cd ../..
git worktree list
git status --short
```
Do not `merge`, `rebase`, `push`, `stash`, `reset --hard`, or `clean` in original checkout.

