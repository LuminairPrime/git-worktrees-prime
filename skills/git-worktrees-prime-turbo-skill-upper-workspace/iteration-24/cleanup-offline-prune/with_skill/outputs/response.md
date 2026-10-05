Sequence for `case02/checkouts/completed` / `task/completed` -> `release`:

1. Inventory canonical paths/branches, do not assume:
```sh
git worktree list --porcelain -z
```
Identify: `case02/checkouts/completed`=`task/completed`, offline-worker path unmounted/colleague-owned, retired scratch path missing, primary.

2. Inspect completed checkout state:
```sh
git -C "case02/checkouts/completed" status --short --branch --untracked-files=all
git -C "case02/checkouts/completed" status --short --ignored
git -C "case02/checkouts/completed" rev-parse HEAD
git -C "case02/checkouts/completed" rev-parse --abbrev-ref HEAD
```
Expect: `task/completed`, squash-integrated tip recorded, `!! review.db` per `references/raw-git-commands.md:46-48`. Check for unfinished merge/rebase/submodule state before proceeding.

3. Resolve current integration ref:
```sh
git rev-parse --verify "release^{commit}"
git rev-parse --verify "task/completed^{commit}"
```

4. Ancestry check — expected to fail for squash, not deletion authority:
```sh
git merge-base --is-ancestor "task/completed" "release"; echo $?
```
Verify squash replacement instead, e.g.:
```sh
git log --oneline -5 release
git diff release...task/completed --stat
```

5. Preserve reviewer-needed ignored file outside deletion path:
```sh
mkdir -p "<preservation-dir-outside-worktree>"
cp -p "case02/checkouts/completed/review.db" "<preservation-dir>/review.db"
ls -l "<preservation-dir>/review.db"
sha256sum "case02/checkouts/completed/review.db" "<preservation-dir>/review.db"
```

6. Leave checkout before removal:
```sh
cd "<primary-root>"
```

7. Remove only exact completed checkout:
```sh
git worktree remove "case02/checkouts/completed"
```
No `rm -rf`, no `-B`, no `--force`. Do not touch offline-worker.

8. Retain branch: skip deletion:
```sh
# DO NOT RUN: git branch -d/-D "task/completed"
```
Reason: review remains open on `task/completed`; squash breaks ancestry so `-d` refusal is expected.

9. Prune only intentionally removed registration:
```sh
git worktree prune --dry-run --verbose
```
Require: lists only retired scratch, not offline-worker. If offline-worker appears, stop — missing dir = unmounted volume, do not prune/unlock/remove it.

10. Same options prune:
```sh
git worktree prune --verbose
```

11. Verify result:
```sh
git worktree list --porcelain -z
test ! -e "case02/checkouts/completed"; echo $?
git show-ref --verify --quiet "refs/heads/task/completed"; echo $?
git branch --list "task/completed"
ls -l "<preservation-dir>/review.db"
```

Report remains:
- Removed: directory `case02/checkouts/completed` + its registration.
- Pruned: retired scratch registration only.
- Retained: branch `task/completed` for open review; preserved `review.db` copy at `<preservation-dir>/review.db`; offline-worker registration + unmounted path untouched, colleague-owned/in-use; primary/`release` unchanged.

