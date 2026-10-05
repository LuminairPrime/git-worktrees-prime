In order, from the parent of `project/`:

1. Inventory, preserve colleague state:
```sh
git -C project worktree list --porcelain -z
git -C project status --short --branch
git -C project rev-parse --verify "release/next^{commit}"
```

2. Require ignore coverage for in-checkout destination, exit `0` required:
```sh
git -C project check-ignore -q -- scratch-checkouts/normalize/
```

3. Create isolated checkout, new branch explicitly from base:
```sh
git -C project worktree add -b task/normalize scratch-checkouts/normalize release/next
```

4. Verify new checkout:
```sh
git -C project/scratch-checkouts/normalize rev-parse --show-toplevel
git -C project/scratch-checkouts/normalize status --short --branch
git -C project/scratch-checkouts/normalize rev-parse HEAD
git -C project check-ignore -q -- scratch-checkouts/normalize/
```

5. In `project/scratch-checkouts/normalize` only, fix `normalize_label` to `strip()` surrounding whitespace and `lower()` result. Do not touch `project/` original, do not stash/reset/clean/pull there.

6. Run project's documented check from task checkout:
```sh
git -C project/scratch-checkouts/normalize status --short --branch
# read check in task checkout README/CONTRIBUTING/Makefile/package.json/pyproject.toml, then run that check in project/scratch-checkouts/normalize
```

7. Commit on task branch:
```sh
git -C project/scratch-checkouts/normalize add -- <fixed-file>
git -C project/scratch-checkouts/normalize status --short --branch
git -C project/scratch-checkouts/normalize commit -m "Fix normalize_label to strip whitespace and lowercase"
git -C project/scratch-checkouts/normalize log -1 --oneline
git -C project/scratch-checkouts/normalize status --short --branch
```

8. Leave for review, no integration:
```sh
git -C project worktree list --porcelain -z
```
Retain `project/scratch-checkouts/normalize` and `task/normalize`. Do not merge, push, remove worktree, delete branch, or prune.

