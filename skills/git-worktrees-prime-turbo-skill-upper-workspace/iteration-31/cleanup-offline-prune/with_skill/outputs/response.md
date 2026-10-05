Exact run order for this finish, per worktree cleanup tree:

`task/completed` is squash-merged to `release` but review is still open: checkout may go, branch must stay.

### 1. Inventory - canonical paths, ownership
```sh
git worktree list --porcelain -z
git rev-parse --show-toplevel
pwd
```
Check: `case02/checkouts/completed` == registered `<completed-abs>` for `task/completed`. Note primary, `offline-worker` (colleague-owned, unmounted, in use), `scratch` (deleted from disk) paths. Do not touch `offline-worker`.

### 2. Inspect completed checkout state
```sh
git -C "<completed-abs>" rev-parse --show-toplevel
git -C "<completed-abs>" branch --show-current
git -C "<completed-abs>" rev-parse HEAD
git -C "<completed-abs>" status --short --branch --untracked-files=all
git -C "<completed-abs>" status --short --ignored
git -C "<completed-abs>" submodule status
```
Check: clean except `!! review.db`; record `HEAD` as `<task-tip>`; no `MERGE_HEAD/CHERRY_PICK_HEAD/rebase-merge` in progress, no detached valuable commit, no nested repo state.

### 3. Verify squash-integration to current `release`
```sh
git rev-parse --verify "release^{commit}"
git rev-parse --verify "task/completed^{commit}"
git merge-base --is-ancestor "<task-tip>" "release"; echo $?
git log --oneline -5 release
```
Check: `merge-base --is-ancestor` is expected non-`0` for squash - not deletion evidence. Verify replacement by content, e.g. squash commit on `release` with same diff.

Do not run `branch -d/-D task/completed`: review open, ancestry broken.

### 4. Preserve reviewer file outside deletion path
```sh
cp "<completed-abs>/review.db" "<safe-outside-path>/review.db"
ls -l "<safe-outside-path>/review.db"
sha256sum "<completed-abs>/review.db" "<safe-outside-path>/review.db"
```
Check: copy succeeds, checksums match. Do not rely on harness archive; ignored files do not follow.

### 5. Leave checkout before removal
```sh
cd "<primary-root>"
pwd
```
Check: `pwd` is not `<completed-abs>`, not its parent to be deleted, not `offline-worker`.

### 6. Remove only exact task checkout
```sh
git worktree remove "<completed-abs>"
```
Do not `rm -rf`, `move`, `repair`, `unlock`, or `prune` to do this.

### 7. Selective prune - only intentionally removed `scratch`
```sh
git worktree prune --dry-run --verbose
```
Check every entry: proceed only if output lists only retired `scratch` path and does NOT list `offline-worker` path. Missing dir can be offline volume.
```sh
# only if above condition holds with same defaults:
git worktree prune --verbose
```
Otherwise: skip pruning. Never `unlock`/prune `offline-worker` because unmounted.

### 8. Verify result
```sh
git worktree list --porcelain -z
test ! -e "<completed-abs>"; echo $?
git show-ref --verify --quiet "refs/heads/task/completed"; echo $?
git rev-parse --verify "release^{commit}"
ls -l "<safe-outside-path>/review.db"
```

### Report what remains
* Removed: checkout `<completed-abs>` (`case02/checkouts/completed`).
* Retained branch: `task/completed` at `<task-tip>` - review open, squash breaks `-d` ancestry check.
* Retained file: `review.db` copy at `<safe-outside-path>/review.db`.
* Retained registration: `offline-worker` - colleague-owned, unmounted, still in use, not pruned/unlocked.
* Pruned registration only: `scratch` - already deleted from disk, confirmed sole dry-run entry.
* Integrated: squash commit(s) on `release`.

