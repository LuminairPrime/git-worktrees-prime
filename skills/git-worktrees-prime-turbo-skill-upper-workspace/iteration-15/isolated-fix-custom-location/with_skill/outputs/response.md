In `project`, colleague checkout stays untouched — all work in new checkout:

1. Inventory + preserve dirty state:
```sh
git -C "project" worktree list --porcelain -z
git -C "project" status --short --branch
```
Check: note uncommitted notes + untracked draft; do not stash/reset/clean/pull/checkout there.

2. Resolve current base:
```sh
git -C "project" fetch origin release/next
git -C "project" rev-parse --verify "release/next^{commit}"
```

3. Require ignore coverage for destination inside checkout, exit `0`:
```sh
git -C "project" check-ignore -q -- "scratch-checkouts/normalize/"
```

4. Create checkout + task branch from base:
```sh
git -C "project" worktree add -b "task/normalize" "project/scratch-checkouts/normalize" "release/next"
```

5. Verify new checkout + repeat ignore check:
```sh
git -C "project/scratch-checkouts/normalize" rev-parse --show-toplevel
git -C "project/scratch-checkouts/normalize" status --short --branch
git -C "project/scratch-checkouts/normalize" rev-parse HEAD
git -C "project" check-ignore -q -- "scratch-checkouts/normalize/"
```

6. Edit only in `project/scratch-checkouts/normalize`: fix `normalize_label` to `strip()` surrounding whitespace and return `.lower()` text.

7. Review + run project check from task checkout:
```sh
git -C "project/scratch-checkouts/normalize" diff -- <file-with-normalize_label>
<project-check>
```
Check: check passes before commit; use repo-documented check command.

8. Commit on `task/normalize`:
```sh
git -C "project/scratch-checkouts/normalize" add <file-with-normalize_label>
git -C "project/scratch-checkouts/normalize" commit -m "Fix normalize_label to strip and lowercase"
```

9. Leave ready for review, no integration:
```sh
git -C "project/scratch-checkouts/normalize" status --short --branch
git -C "project/scratch-checkouts/normalize" log -1 --oneline
git -C "project" worktree list --porcelain -z
git -C "project" status --short --branch
```
Stop: retain `project/scratch-checkouts/normalize` + `task/normalize`; no merge, push, `remove`, `branch -d`, or `prune`.

