Exact sequence, in order. `<repo>` = current colleague checkout. Do not modify it:

1. Confirm ownership / starting state:
```sh
pwd
git worktree list --porcelain -z
git status --short --branch
git branch --show-current
```

2. Verify destination will be isolated and ignored:
```sh
git rev-parse --path-format=absolute --git-path info/exclude
git check-ignore -q -- "project/scratch-checkouts/normalize/"
```
Require exit `0`. If non-zero, add `project/scratch-checkouts/normalize/` to that exclude file first. Do not proceed unignored.

3. Resolve requested base without touching colleague checkout — fetch only, no `pull`, `checkout`, `stash`, `reset`, `clean` in `<repo>`:
```sh
git -C "<repo>" fetch origin release/next
git -C "<repo>" rev-parse --verify "release/next^{commit}"
```

4. Create separate checkout:
```sh
git -C "<repo>" worktree add -b "task/normalize" "project/scratch-checkouts/normalize" "release/next"
```
Do not use `-B`.

5. Verify new checkout:
```sh
git -C "project/scratch-checkouts/normalize" rev-parse --show-toplevel
git -C "project/scratch-checkouts/normalize" status --short --branch
git -C "project/scratch-checkouts/normalize" rev-parse HEAD
git -C "project/scratch-checkouts/normalize" log --oneline -1
git check-ignore -q -- "project/scratch-checkouts/normalize/"
```

6. In `project/scratch-checkouts/normalize` only, locate and fix:
```sh
grep -rn "normalize_label" .
```
Edit to strip + lowercase, e.g. `return text.strip().lower()`.

7. Run project's documented check from task checkout only:
```sh
git -C "project/scratch-checkouts/normalize" status --short --branch
```
Then run check, e.g. `pytest` / `npm test` / `make check` per repo docs. Require pass.

8. Commit on task branch:
```sh
git -C "project/scratch-checkouts/normalize" add <fixed-file>
git -C "project/scratch-checkouts/normalize" status --short --branch
git -C "project/scratch-checkouts/normalize" commit -m "Fix normalize_label to strip whitespace and lowercase"
```

9. Leave ready for review, verify no integration:
```sh
git -C "project/scratch-checkouts/normalize" log --oneline -3
git -C "project/scratch-checkouts/normalize" status --short --branch
git worktree list --porcelain -z
```
Stop here. No merge, no push, no PR, no `worktree remove`, no `branch -d`, no `prune`. Original checkout's notes/draft remain intact.

