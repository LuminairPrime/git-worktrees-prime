In `project/` checkout, do not modify colleague state — no `stash/reset/clean/pull/checkout`:

1. Record context:
```sh
pwd
git rev-parse --show-toplevel
git worktree list --porcelain -z
git -C "." status --short --branch
git -C "." branch --show-current
```
2. Verify ignore coverage for requested path inside checkout:
```sh
git rev-parse --path-format=absolute --git-path info/exclude
git -C "." check-ignore -q -- "scratch-checkouts/normalize/"
```
Require exit `0`; if not ignored, add `scratch-checkouts/` per repo convention and re-check. Do not proceed inside another checkout without this.

3. Resolve requested base without touching current checkout:
```sh
git -C "." fetch origin release/next
git -C "." rev-parse --verify "release/next^{commit}"
```

4. Create isolated checkout + task branch from base:
```sh
git -C "." worktree add -b "task/normalize" "scratch-checkouts/normalize" "release/next"
```

5. Verify new checkout, branch, and ignore:
```sh
git -C "scratch-checkouts/normalize" rev-parse --show-toplevel
git -C "scratch-checkouts/normalize" status --short --branch
git -C "scratch-checkouts/normalize" rev-parse HEAD
git -C "scratch-checkouts/normalize" log --oneline -3
git -C "." check-ignore -q -- "scratch-checkouts/normalize/"
git -C "." worktree list --porcelain -z
```

6. Fix in `scratch-checkouts/normalize` only, e.g.:
```py
return label.strip().lower()
```

7. Run project's documented check from task checkout:
```sh
git -C "scratch-checkouts/normalize" status --short --branch
# run repo check, e.g. pytest/npm test/make check per README/CONTRIBUTING
```

8. Commit on `task/normalize`, leave unpushed for review:
```sh
git -C "scratch-checkouts/normalize" diff -- label
git -C "scratch-checkouts/normalize" add -- <file-containing-normalize_label>
git -C "scratch-checkouts/normalize" status --short --branch
git -C "scratch-checkouts/normalize" commit -m "Fix normalize_label to strip and lowercase"
git -C "scratch-checkouts/normalize" log --oneline -3
git -C "scratch-checkouts/normalize" status --short --branch
git -C "." worktree list --porcelain -z
```
Stop: original notes/draft untouched, no merge, no push.

