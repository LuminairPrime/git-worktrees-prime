In order, from the current checkout (`<primary-root>`). Do not modify it:

1. Inventory, confirm dirty state to preserve:
```sh
git worktree list --porcelain -z
git status --short --branch
git rev-parse --show-toplevel
```

2. Verify ignore coverage for requested path inside checkout, require exit `0` before creation:
```sh
git rev-parse --path-format=absolute --git-path info/exclude
git check-ignore -q -- project/scratch-checkouts/normalize/
```
If non-zero: add `project/scratch-checkouts/` to ignore, then repeat.

3. Establish current base, do not `pull`/`reset`/`stash`/`clean` the colleague checkout:
```sh
git fetch origin release/next
git rev-parse --verify "release/next^{commit}"
git rev-parse --verify "origin/release/next^{commit}"
```

4. Create separate checkout with new branch, do not use `-B`:
```sh
git worktree add -b task/normalize project/scratch-checkouts/normalize release/next
```

5. Verify new checkout:
```sh
git -C project/scratch-checkouts/normalize rev-parse --show-toplevel
git -C project/scratch-checkouts/normalize status --short --branch
git -C project/scratch-checkouts/normalize rev-parse HEAD
git check-ignore -q -- project/scratch-checkouts/normalize/
```

6. Edit only in new checkout: fix `normalize_label` to strip surrounding whitespace and lowercase, e.g. `return label.strip().lower()`.

7. Run project check from new checkout only:
```sh
git -C project/scratch-checkouts/normalize status --short --branch
# run repo-documented check, e.g.:
git -C project/scratch-checkouts/normalize rev-parse --show-toplevel
```

8. Commit on task branch:
```sh
git -C project/scratch-checkouts/normalize diff -- <file>
git -C project/scratch-checkouts/normalize add -- <file>
git -C project/scratch-checkouts/normalize commit -m "Fix normalize_label to strip and lowercase"
git -C project/scratch-checkouts/normalize log --oneline -3
git -C project/scratch-checkouts/normalize status --short --branch
git worktree list --porcelain -z
```

9. Stop, ready for review. No merge, no push, no `worktree remove`, no `branch -d`, no `worktree prune`.

