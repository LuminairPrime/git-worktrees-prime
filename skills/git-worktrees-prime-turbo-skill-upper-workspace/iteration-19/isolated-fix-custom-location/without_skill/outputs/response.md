In order, from parent of `project/`, original checkout untouched:

1. Verify colleague checkout read-only:
```bash
git -C project status --short --branch --untracked-files=all
git -C project branch --show-current
git -C project log --oneline -1 release/next
```

2. Fetch base, create separate checkout:
```bash
git -C project fetch origin release/next --prune
git -C project worktree add ./scratch-checkouts/normalize -b task/normalize release/next
```

3. Work only in new checkout:
```bash
cd project/scratch-checkouts/normalize
git branch --show-current
git log --oneline -1
git status --short --branch
grep -rn "def normalize_label" .
```

4. Fix `normalize_label` to:
```python
return text.strip().lower()
```

5. Verify + run project check:
```bash
git diff
python3 -c "from <module> import normalize_label; assert normalize_label('  HeLLo  ')== 'hello'"
python -m pytest -q
```

6. Commit on task branch:
```bash
git status --short
git add <file-with-normalize_label-only>
git commit -m "fix: strip whitespace and lowercase in normalize_label"
git status --short --branch
git log --oneline -2
git worktree list
```

Left ready: `project/scratch-checkouts/normalize` on `task/normalize`, committed. Original `project` notes/draft untouched. No `stash/reset/clean/switch` in original, no merge/push.
