Isolated fix plan — no work in colleague checkout:

1. Inventory and preserve current checkout:
```sh
git -C "project" worktree list --porcelain -z
git -C "project" status --short --branch
git -C "project" rev-parse --verify "release/next^{commit}"
```
Expect: unrelated modified notes + untracked draft visible. Do not stash, reset, clean, pull, or checkout here.

2. Verify nested path is ignored before creation:
```sh
git -C "project" rev-parse --path-format=absolute --git-path info/exclude
git -C "project" check-ignore -q -- "scratch-checkouts/normalize/"
```
Require exit `0`. If not ignored, add exclusion first, do not create.

3. Create task checkout:
```sh
git -C "project" worktree add -b "task/normalize" "project/scratch-checkouts/normalize" "release/next"
```

4. Verify new checkout:
```sh
git -C "project/scratch-checkouts/normalize" rev-parse --show-toplevel
git -C "project/scratch-checkouts/normalize" status --short --branch
git -C "project/scratch-checkouts/normalize" rev-parse HEAD
git -C "project" check-ignore -q -- "scratch-checkouts/normalize/"
```
Expect: `task/normalize` on `release/next` commit, clean status.

5. In `project/scratch-checkouts/normalize` only: locate `normalize_label`, edit to `strip()` surrounding whitespace and return lowercase, e.g. `return label.strip().lower()`.

6. Run project check from task checkout and review diff:
```sh
git -C "project/scratch-checkouts/normalize" status --short --branch
# run repo-documented check, e.g. pytest / npm test / make check
git -C "project/scratch-checkouts/normalize" diff
```

7. Commit task change only:
```sh
git -C "project/scratch-checkouts/normalize" add <file-containing-normalize_label>
git -C "project/scratch-checkouts/normalize" commit -m "Fix normalize_label to strip and lowercase"
git -C "project/scratch-checkouts/normalize" log -1 --oneline
git -C "project/scratch-checkouts/normalize" status --short --branch
```

8. Leave ready for review:
```sh
git -C "project" worktree list --porcelain -z
```
Retain `project/scratch-checkouts/normalize` + `task/normalize`. Do not merge, push, `worktree remove`, `branch -d/-D`, `worktree prune`, `worktree move`, or `-B` reset.

