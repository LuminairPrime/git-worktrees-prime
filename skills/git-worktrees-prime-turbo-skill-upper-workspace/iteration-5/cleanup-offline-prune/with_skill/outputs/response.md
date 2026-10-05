1. Confirm registrations, canonical paths, ownership:
```sh
git -C "case02/checkouts/completed" worktree list --porcelain -z
pwd
```

2. Inspect `case02/checkouts/completed` state — tracked/untracked, ignored `review.db`, tip, unfinished operation:
```sh
git -C "case02/checkouts/completed" status --short --branch --untracked-files=all
git -C "case02/checkouts/completed" status --short --ignored
git -C "case02/checkouts/completed" rev-parse HEAD
ls -l "case02/checkouts/completed/review.db"
```

3. Preserve reviewer state outside deletion path before removal, verify:
```sh
cp -a "case02/checkouts/completed/review.db" "<preserve-dir-outside-worktree>/review.db"
ls -l "<preserve-dir-outside-worktree>/review.db"
sha256sum "case02/checkouts/completed/review.db" "<preserve-dir-outside-worktree>/review.db"
```

4. Verify squash-integration into current `release`; expect non-ancestry:
```sh
git -C "case02/checkouts/completed" rev-parse --verify "task/completed^{commit}"
git -C "case02/checkouts/completed" rev-parse --verify "release^{commit}"
git -C "case02/checkouts/completed" merge-base --is-ancestor "task/completed" "release"; echo $?
git -C "case02/checkouts/completed" log --oneline -5 release
```
Manually confirm squash commit content matches `task/completed` changes. Do not use `branch -d` success as integration proof.

5. Leave checkout, remove only exact task checkout via Git:
```sh
cd "<primary-root-or-other-surviving-checkout>"
git -C "<primary-root-or-other-surviving-checkout>" worktree remove "case02/checkouts/completed"
```

6. Retain branch: do NOT run `git branch -d task/completed` — open review needs it, squash breaks ancestry.

7. Verify removal and branch retention:
```sh
git worktree list --porcelain -z
test ! -e "case02/checkouts/completed"; echo $?
git show-ref --verify --quiet "refs/heads/task/completed"; echo $?
```

8. Dry-run prune only, review each entry, do NOT prune:
```sh
git worktree prune --dry-run --verbose
```
Expected: `retired scratch` = intentionally deleted, prunable; `offline-worker` = missing only because share unmounted, colleague-owned/in-use — must not prune/unlock. Mixed set: run no `prune --verbose`.

Report remains: removed `case02/checkouts/completed`; retained branch `task/completed` for open review, preserved `review.db` at `<preserve-dir-outside-worktree>/review.db`, retained registrations for `offline-worker` and `retired scratch`, no prune/branch delete performed.

