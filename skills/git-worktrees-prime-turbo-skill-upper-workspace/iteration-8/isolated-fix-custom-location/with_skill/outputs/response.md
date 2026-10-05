Planned sequence — raw Git, no harness assumed:

1. Inventory — do not modify colleague checkout:
```sh
git -C project worktree list --porcelain -z
git -C project status --short --branch --untracked-files=all
```

2. Resolve requested base `release/next`, without `pull` into colleague checkout:
```sh
git -C project fetch origin release/next
git -C project rev-parse --verify "release/next^{commit}"
```

3. Verify ignore coverage for checkout-inside-checkout, require exit `0` before creation:
```sh
git -C project rev-parse --path-format=absolute --git-path info/exclude
git -C project check-ignore -q -- scratch-checkouts/normalize/
```
If non-zero: add `scratch-checkouts/` to ignore via repo convention/local exclude, then repeat check. Do not proceed unignored.

4. Create separate checkout on new task branch from base — use `-b`, not `-B`:
```sh
git -C project worktree add -b task/normalize project/scratch-checkouts/normalize release/next
```

5. Verify new checkout:
```sh
git -C project/scratch-checkouts/normalize rev-parse --show-toplevel
git -C project/scratch-checkouts/normalize status --short --branch
git -C project/scratch-checkouts/normalize rev-parse HEAD
git -C project check-ignore -q -- scratch-checkouts/normalize/
```

6. Develop only in `project/scratch-checkouts/normalize`:
- Follow that checkout's README/CONTRIBUTING for setup; do not bulk-copy ignored deps/secrets/build outputs from colleague checkout.
- Do not transfer/stash/reset/clean colleague's uncommitted notes + untracked draft.
- Fix `normalize_label` to `strip()` surrounding whitespace then `lower()` return.

7. Run project's documented check from task checkout, e.g. lint/test target per repo docs; fix failures.

8. Review then commit on `task/normalize`:
```sh
git -C project/scratch-checkouts/normalize diff
git -C project/scratch-checkouts/normalize status --short --branch --untracked-files=all
git -C project/scratch-checkouts/normalize add <file-containing-normalize_label>
git -C project/scratch-checkouts/normalize commit -m "Fix normalize_label to strip whitespace and lowercase"
git -C project/scratch-checkouts/normalize log --oneline -1
git -C project/scratch-checkouts/normalize status --short --branch
```

9. Leave ready for review, no integration:
```sh
git -C project worktree list --porcelain -z
```
Retain: checkout `project/scratch-checkouts/normalize`, branch `task/normalize`, base `release/next`. No merge, no push, no `worktree remove`, no `branch -d`, no `prune`.

