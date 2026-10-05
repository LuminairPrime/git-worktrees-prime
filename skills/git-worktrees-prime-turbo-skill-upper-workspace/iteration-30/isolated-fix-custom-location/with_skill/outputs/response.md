In `project/` primary checkout — leave dirty state intact:

1. Inventory, do not modify:
```sh
git worktree list --porcelain -z
git status --short --branch
git rev-parse --verify "release/next^{commit}"
```
Documents colleague's uncommitted notes + untracked draft. Do not stash/reset/clean/pull.

2. Require ignored destination, exit `0` before creation:
```sh
git check-ignore -q -- "scratch-checkouts/normalize/"
```

3. Create separate checkout:
```sh
git worktree add -b "task/normalize" "scratch-checkouts/normalize" "release/next"
```

4. Verify new checkout:
```sh
git -C "scratch-checkouts/normalize" rev-parse --show-toplevel
git -C "scratch-checkouts/normalize" status --short --branch
git -C "scratch-checkouts/normalize" rev-parse HEAD
git check-ignore -q -- "scratch-checkouts/normalize/"
```

5. Fix in task checkout only — `normalize_label` to `strip()` surrounding whitespace and `lower()`:
```sh
# edit definition in scratch-checkouts/normalize, e.g. return label.strip().lower()
```

6. Run project check from task checkout:
```sh
git -C "scratch-checkouts/normalize" status --short --branch
# repo's check/test command, run in scratch-checkouts/normalize
```

7. Commit on `task/normalize`, leave for review — no merge/push/prune:
```sh
git -C "scratch-checkouts/normalize" add <fixed-file>
git -C "scratch-checkouts/normalize" commit -m "Fix normalize_label to strip and lowercase"
git -C "scratch-checkouts/normalize" rev-parse HEAD
git -C "scratch-checkouts/normalize" status --short --branch
git worktree list --porcelain -z
```
Retain `scratch-checkouts/normalize` + `task/normalize`. Base: `release/next`.
