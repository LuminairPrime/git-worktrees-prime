1. Establish inventory from surviving checkout, do not remove `cwd`:

```sh
pwd
git rev-parse --show-toplevel
git worktree list --porcelain -z
```

Check: canonical absolute path for `case02/checkouts/completed`, its branch is `task/completed`, its `HEAD`; identify `offline-worker` missing/unmounted vs `scratch` missing/deleted, primary checkout, current directory.

2. Inspect state to be reclaimed in exact checkout:

```sh
git -C "case02/checkouts/completed" branch --show-current
git -C "case02/checkouts/completed" rev-parse HEAD
git -C "case02/checkouts/completed" status --short --branch --untracked-files=all
git -C "case02/checkouts/completed" status --short --ignored
git -C "case02/checkouts/completed" submodule status
```

Check: tracked/untracked changes, ignored `review.db` present, no detached `HEAD`, no `MERGE_HEAD/CHERRY_PICK_HEAD/rebase-merge` in progress.

3. Preserve reviewer-needed ignored state outside deletion path:

```sh
mkdir -p "<preservation-dir-outside-case02/checkouts/completed>"
cp -p "case02/checkouts/completed/review.db" "<preservation-dir>/review.db"
ls -l "<preservation-dir>/review.db"
sha256sum "case02/checkouts/completed/review.db" "<preservation-dir>/review.db"
```

Do not rely on archive; `git worktree remove` deletes `review.db`.

4. Verify integration target, squash breaks ancestry:

```sh
git rev-parse --verify "task/completed^{commit}"
git rev-parse --verify "release^{commit}"
git merge-base --is-ancestor "task/completed" "release"; echo $?
git log --oneline -5 release
git diff release...task/completed --stat
```

Expected: `merge-base --is-ancestor` non-zero due to squash-integrated; verify replacement commits/changes manually. Do not use `branch -d` success as evidence.

5. Leave directory, remove only exact checkout via manager:

```sh
cd "<primary-root>"
git -C "<primary-root>" worktree remove "/abs/path/to/case02/checkouts/completed"
```

No `rm -rf`, no `--force`, no `move`, no primary/`cwd`/parent/sibling path.

6. Explicitly retain branch for open review:

```sh
# NOT RUN: git branch -d task/completed
# NOT RUN: git branch -D task/completed
git show-ref --verify --quiet "refs/heads/task/completed"; echo $?
```

Reason: review remains open on `task/completed`; squash ancestry is broken.

7. Verify removal, retain refs:

```sh
git worktree list --porcelain -z
test ! -e "/abs/path/to/case02/checkouts/completed"; echo $?
git branch --list "task/completed"
ls -l "<preservation-dir>/review.db"
```

8. Stale metadata dry-run only:

```sh
git worktree prune --dry-run --verbose
```

Expected entries: `offline-worker` unmounted/colleague-owned/in-use + retired `scratch` deleted. Since not every entry is intentionally removed, do not prune. Missing dir may be offline volume.

```sh
# NOT RUN: git worktree prune --verbose
git worktree list --porcelain -z
```

Remains reported:
* removed: `case02/checkouts/completed` checkout registration + directory.
* retained: branch `task/completed` for open review; `<preservation-dir>/review.db` copy for reviewer; `offline-worker` registration unpruned/unmounted colleague-owned in-use; `scratch` stale registration unpruned because mixed dry-run forbids pruning.

