Reclaim `case02/checkouts/completed` / `task/completed`, retain review state:

1. Inventory canonical paths/ownership:
```sh
git worktree list --porcelain -z
git -C "case02/checkouts/completed" rev-parse --show-toplevel
git -C "case02/checkouts/completed" rev-parse HEAD
git -C "case02/checkouts/completed" status --short --branch --untracked-files=all
```

2. Find disappearing state:
```sh
git -C "case02/checkouts/completed" status --short --ignored
# confirms ignored review.db
```

3. Verify squash-integration; ancestry check is expected to fail for squash:
```sh
git rev-parse --verify "task/completed^{commit}"
git rev-parse --verify "release^{commit}"
git merge-base --is-ancestor "task/completed" "release"; echo $?
# non-zero needs manual review: verify replacement commits/diff on release contains task changes
```

Do not use `branch -d` success as integration proof. Do not delete `task/completed`: review remains open.

4. Preserve needed ignored file outside deletion path before removal:
```sh
cp -p "case02/checkouts/completed/review.db" "<safe-path-outside-worktree>/review.db"
ls -l "<safe-path-outside-worktree>/review.db"
```

5. From surviving primary checkout, not inside target, remove only exact checkout:
```sh
cd "<primary-root>"
git -C "<primary-root>" worktree remove "<absolute-path-to-case02/checkouts/completed>"
```

Do not `rm -rf` directory, do not `worktree move`, do not touch colleague-owned offline-worker checkout.

6. Verify removal and retained branch:
```sh
git worktree list --porcelain -z
test ! -e "case02/checkouts/completed" && echo "removed"
git show-ref --verify --quiet "refs/heads/task/completed" && echo "branch-retained"
```

Do not run `branch -d/-D task/completed`.

7. Check stale metadata, do not prune:
```sh
git worktree prune --dry-run --verbose
# expected: lists retired scratch + unmounted offline-worker as missing
# abort: do NOT run `worktree prune --verbose`
```

Reason: every dry-run entry is not intentionally removed. Offline share is unmounted but still in use/colleague-owned.

Remains:
* removed: `case02/checkouts/completed` registration/directory.
* retained: branch `task/completed` for open review.
* retained: `review.db` copy at `<safe-path-outside-worktree>/review.db`.
* retained: offline-worker registration, still in use, unmounted.
* retained: retired scratch stale registration, not pruned to avoid pruning offline-worker.

