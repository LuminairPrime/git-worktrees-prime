Work in `project/scratch-checkouts/normalize` on branch `task/normalize` from `release/next`. Keep colleague checkout `project` intact. No merge/publish.

1. Inventory source checkout, do not modify:
```sh
git -C "project" worktree list --porcelain -z
git -C "project" status --short --branch
```
Check: confirms unrelated modified notes + untracked draft. Stop if active rebase/merge/bisect. Do not stash, reset, clean, pull.

2. Resolve base, do not pull into `project`:
```sh
git -C "project" fetch origin
git -C "project" rev-parse --verify "release/next^{commit}"
```

3. Verify ignore coverage for in-checkout destination, require exit 0:
```sh
git -C "project" rev-parse --path-format=absolute --git-path info/exclude
git -C "project" check-ignore -q -- "scratch-checkouts/normalize/"
```
If non-zero: add ignore coverage first, then repeat.

4. Create linked checkout + new branch:
```sh
git -C "project" worktree add -b "task/normalize" "project/scratch-checkouts/normalize" "release/next"
```

5. Verify task checkout:
```sh
git -C "project/scratch-checkouts/normalize" rev-parse --show-toplevel
git -C "project/scratch-checkouts/normalize" status --short --branch
git -C "project/scratch-checkouts/normalize" rev-parse HEAD
git -C "project" check-ignore -q -- "scratch-checkouts/normalize/"
```
Check: toplevel == task path, branch `task/normalize`, HEAD == `release/next`, clean.

6. Fix in task checkout only:
- edit `normalize_label` to `strip()` surrounding whitespace then `lower()`.
- run documented check from task path, e.g.:
```sh
git -C "project/scratch-checkouts/normalize" status --short --branch
```

7. Commit on task branch:
```sh
git -C "project/scratch-checkouts/normalize" add <changed-files>
git -C "project/scratch-checkouts/normalize" status --short --branch
git -C "project/scratch-checkouts/normalize" commit -m "Fix normalize_label to strip and lowercase"
git -C "project/scratch-checkouts/normalize" log --oneline -3
git -C "project" worktree list --porcelain -z
```

Retained for review: checkout `project/scratch-checkouts/normalize`, branch `task/normalize`. No `merge`, no `push`, no `worktree remove`, no `branch -d`, no `prune`.

