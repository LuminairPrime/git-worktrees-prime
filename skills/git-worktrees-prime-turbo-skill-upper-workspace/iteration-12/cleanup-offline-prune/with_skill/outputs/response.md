1. Inventory - confirm canonical path/owner, do not guess:
```sh
git worktree list --porcelain -z
```
Expect: primary, `.../case02/checkouts/completed` on `task/completed`, offline-worker path on unmounted share, `scratch` path missing. Use absolute path from this output as `<completed>` below.

2. Inspect loss-risk state in target only:
```sh
git -C "<completed>" status --short --branch --untracked-files=all
git -C "<completed>" status --short --ignored
git -C "<completed>" rev-parse HEAD
```
Expect: `!! review.db` - ignored, reviewer still needs. Record `HEAD` as `<task-tip>`.

3. Verify integration target, do not use `branch -d` as proof:
```sh
git rev-parse --verify "release^{commit}"
git merge-base --is-ancestor "<task-tip>" "release"; echo $?
```
Expected non-zero: squash breaks ancestry. Manually verify replacement commits/diff. Review remains open on `task/completed` -> branch must be retained.

4. Preserve outside deletion path - ignored files are not kept by `remove`/archive:
```sh
cp "<completed>/review.db" "<preservation-dir-outside-completed>/review.db"
ls -l "<preservation-dir-outside-completed>/review.db"
```

5. Reclaim only exact task checkout, from survivor, after leaving it:
```sh
cd "<primary-root>"
git -C "<primary-root>" worktree remove "<completed>"
```
Do not `rm -rf`, do not touch offline-worker, primary, parent, siblings.

6. Retain branch - do not delete:
```sh
# DO NOT RUN: git branch -d task/completed
git show-ref --verify --quiet "refs/heads/task/completed"
git branch -vv --list "task/completed"
```

7. Stale metadata check - dry-run only:
```sh
git -C "<primary-root>" worktree prune --dry-run --verbose
```
Entries will include intentionally-deleted `scratch` AND unmounted but still-in-use offline-worker. Since not every entry is intentionally removed:
```sh
# DO NOT RUN: git worktree prune --verbose
# DO NOT unlock offline-worker
```

8. Verify result:
```sh
git worktree list --porcelain -z
test ! -e "<completed>"; echo $?
git show-ref --verify "refs/heads/task/completed"
ls -l "<preservation-dir-outside-completed>/review.db"
```

Report remains:
* Removed: checkout `<completed>` only.
* Retained: branch `task/completed` - open review, squash-integrated to `release`.
* Retained: `review.db` copy at `<preservation-dir-outside-completed>/review.db`.
* Retained: offline-worker registration - colleague-owned, unmounted, still in use.
* Retained: `scratch` stale registration - prune blocked by offline-worker entry.

