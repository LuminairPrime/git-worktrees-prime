Plan - separate checkout, no touch to current dirty tree:

1. Read-only check of current checkout:
```
pwd
git -C project status --short --branch
git -C project branch --show-current
git -C project log --oneline -3 release/next
git -C project diff --stat
```
Do not `checkout/switch/stash/reset/clean/add` in `project/`.

2. Update base ref only, no working tree change:
```
git -C project fetch origin release/next
```

3. Create separate checkout on new branch from `release/next`:
```
mkdir -p project/scratch-checkouts
git -C project worktree list
git -C project worktree add scratch-checkouts/normalize -b task/normalize release/next
```

4. Verify new checkout:
```
git -C project/scratch-checkouts/normalize branch --show-current
git -C project/scratch-checkouts/normalize log --oneline -1
git -C project/scratch-checkouts/normalize status --short --branch
```

5. Locate `normalize_label` in new checkout only:
```
grep -Rn "normalize_label" project/scratch-checkouts/normalize --exclude-dir=.git
```

6. Edit that file in `project/scratch-checkouts/normalize` to:
```python
return label.strip().lower()
```
Verify diff:
```
git -C project/scratch-checkouts/normalize diff
```

7. Run project's check from new checkout:
```
git -C project/scratch-checkouts/normalize status --short
# inspect check entrypoint, e.g. README/Makefile/pyproject.toml/package.json, then run it, e.g.:
project/scratch-checkouts/normalize/... check command
```
Must pass before commit. Also quick behavior check:
```
python3 -c "from <module> import normalize_label; assert normalize_label('  HeLLo  ')=='hello'"
```

8. Commit only fix on task branch:
```
git -C project/scratch-checkouts/normalize add <file-with-normalize_label>
git -C project/scratch-checkouts/normalize status --short
git -C project/scratch-checkouts/normalize commit -m "Fix normalize_label to strip and lowercase"
```

9. Leave ready for review, no merge/publication:
```
git -C project/scratch-checkouts/normalize branch --show-current
git -C project/scratch-checkouts/normalize log --oneline -2
git -C project/scratch-checkouts/normalize status --short --branch
git -C project worktree list
```
Do not `merge`, `push`, `gh pr create`.

10. Confirm original checkout intact:
```
git -C project status --short --branch
```
Uncommitted notes + untracked draft must still be present.

