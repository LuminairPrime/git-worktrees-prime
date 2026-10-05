1. Confirm canonical paths/ownership - do not assume `case02/checkouts/completed`:

```sh
git -C "<repo>" worktree list --porcelain -z
```

> `<repo>` = surviving checkout/bare repo, e.g. primary. Resolve exact absolute `<worktree>=case02/checkouts/completed`, its `HEAD`/`task/completed`, `offline-worker` entry, `scratch` entry.

2. Inspect what would disappear with the directory:

```sh
git -C "case02/checkouts/completed" status --short --branch --untracked-files=all
git -C "case02/checkouts/completed" status --short --ignored
git -C "case02/checkouts/completed" rev-parse HEAD
test -f "case02/checkouts/completed/review.db" && ls -l "case02/checkouts/completed/review.db"
```

> Expect: ignored `review.db` present. Clean `status` does not prove ignored/detached state safe.

3. Verify integration target, current ref:

```sh
git -C "<repo>" rev-parse --verify "release^{commit}"
git -C "<repo>" merge-base --is-ancestor "<task-tip-from-2>" "release"; echo $?
```

> Expected non-zero: squash breaks ancestry. Not deletion authority. Verify squash result separately e.g. `log/diff release` contains replacement commits. Retain `task/completed` because review remains open - closed/squashed PR alone is insufficient.

4. Preserve reviewer state outside deletion path before removal:

```sh
mkdir -p "<preservation-dir-outside-case02/checkouts/completed>"
cp "case02/checkouts/completed/review.db" "<preservation-dir>/review.db"
ls -l "<preservation-dir>/review.db"
```

> Do not bulk-copy other ignored outputs. Do not leave inside `<worktree>`.

5. Leave directory to be removed, run from survivor:

```sh
pwd
cd "<primary-root>"
git -C "<repo>" worktree remove "case02/checkouts/completed"
```

> Exact checkout only. No `rm -rf`, no `move`, no `--force`, no sibling/parent/primary/current-dir. Do not touch colleague `offline-worker`.

6. Branch deletion: explicitly SKIP:

```sh
# DO NOT RUN: git -C "<repo>" branch -d "task/completed"
git -C "<repo>" show-ref --verify --quiet "refs/heads/task/completed"
```

> Reason: pending review needs branch. `branch -d` checks upstream, not `release`, and would refuse after squash in any case.

7. Stale metadata dry-run only - then STOP:

```sh
git -C "<repo>" worktree prune --dry-run --verbose
# DO NOT RUN: git -C "<repo>" worktree prune --verbose
```

> Reason: dry-run will list `scratch` intentionally deleted + `offline-worker` unmounted colleague-owned still in use. Prune requires every entry be intentionally removed. Missing dir may be offline volume. Do not prune/unlock `offline-worker`.

8. Verify result:

```sh
git -C "<repo>" worktree list --porcelain -z
test ! -e "case02/checkouts/completed" && echo "completed removed"
git -C "<repo>" show-ref --verify --quiet "refs/heads/task/completed" && echo "task/completed retained"
ls -l "<preservation-dir>/review.db"
```

Report remains:

* Removed: checkout `case02/checkouts/completed` only.
* Retained: branch `task/completed` - pending review; `review.db` copy at `<preservation-dir>/review.db`; registration for `offline-worker` - colleague-owned, unmounted, in use; registration for retired `scratch` - stale on disk but unpruned to avoid pruning `offline-worker`.

