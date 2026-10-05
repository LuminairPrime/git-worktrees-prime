Reclaim `case02/checkouts/completed` only, retain `task/completed` for review:

1. Inventory, ownership:
```sh
git worktree list --porcelain -z
pwd
git rev-parse --show-toplevel
```
Check: current shell not in `case02/checkouts/completed`; `completed`, offline colleague-owned, deleted `scratch` identified; primary excluded.

2. Inspect disappearing state in target checkout:
```sh
git -C "case02/checkouts/completed" status --short --branch --untracked-files=all
git -C "case02/checkouts/completed" status --short --ignored
git -C "case02/checkouts/completed" rev-parse HEAD
ls -l "case02/checkouts/completed/review.db"
```
Check: tracked clean, unfinished merge/rebase resolved, `review.db` present as ignored.

3. Integration check — expect non-0 for squash:
```sh
git merge-base --is-ancestor "task/completed" "release"; echo $?
```
Check: squash breaks ancestry, `branch -d` is not integration evidence; retain branch because review open on `task/completed`.

4. Preserve outside deletion path — `remove` deletes ignored files:
```sh
mkdir -p "<preserve-dir-outside-worktree>"
cp "case02/checkouts/completed/review.db" "<preserve-dir-outside-worktree>/review.db"
ls -l "<preserve-dir-outside-worktree>/review.db"
```

5. Remove exact checkout only, from survivor, no force, no `rm -rf`:
```sh
git -C "<primary-root>" worktree remove "case02/checkouts/completed"
```

6. Verify removal, retain branch:
```sh
git worktree list --porcelain -z
test ! -e "case02/checkouts/completed"; echo $?
git show-ref --verify --quiet "refs/heads/task/completed"; echo $?
git branch --list "task/completed"
```

7. Stale metadata dry-run only:
```sh
git worktree prune --dry-run --verbose
```
Check: entries = intentionally deleted `scratch` + unmounted but in-use offline-worker. Do NOT run `worktree prune --verbose`, do NOT unlock, do NOT delete `task/completed` with `-d/-D`.

Remains:
- Removed: `case02/checkouts/completed` directory/registration.
- Retained: branch `task/completed` for open review; `review.db` copy at `<preserve-dir-outside-worktree>/review.db`; primary checkout; offline-worker registration untouched — unmounted, colleague-owned, in use; `scratch` stale registration — prune deferred until offline-worker available.

