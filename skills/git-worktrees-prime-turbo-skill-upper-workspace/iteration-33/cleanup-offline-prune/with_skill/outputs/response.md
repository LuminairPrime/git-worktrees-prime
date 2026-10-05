Sequence of commands and checks, in order (placeholders: `<repo>` = primary checkout root; `<db>` = path of `review.db` inside the completed checkout; `<offline>` = offline-worker checkout path on the unmounted share; `<scratch>` = retired scratch checkout path):

## 1. Establish inventory and locate the repo

```sh
git -C "case02/checkouts/completed" rev-parse --git-common-dir
git -C "<repo>" worktree list --porcelain -z
```
Confirm the three registrations: completed (branch `task/completed`), offline-worker (on the unmounted share), scratch (directory already gone). Note each one's branch, lock state (`locked <reason>`), and absolute path.

## 2. Inspect the completed checkout before removing it

```sh
git -C "case02/checkouts/completed" branch --show-current
git -C "case02/checkouts/completed" rev-parse HEAD
git -C "case02/checkouts/completed" status --short --branch --untracked-files=all
git -C "case02/checkouts/completed" status --short --ignored
git -C "case02/checkouts/completed" submodule status
git -C "case02/checkouts/completed" rev-parse --git-path MERGE_HEAD   # test -f: none, i.e. no unfinished op
```
Expected: branch `task/completed`, no tracked modifications, only the ignored `review.db`, no submodules, no in-progress merge/rebase.

## 3. Confirm `review.db` is the ignored file and locate it

```sh
git -C "case02/checkouts/completed" check-ignore -v -- "<db>"
ls -l "case02/checkouts/completed/<db>"
sha256sum "case02/checkouts/completed/<db>"
```
Exit 0 from `check-ignore` confirms ignored. Record the checksum.

## 4. Verify how `task/completed` relates to `release`

```sh
git -C "<repo>" rev-parse --verify "task/completed^{commit}"
git -C "<repo>" rev-parse --verify "release^{commit}"
git -C "<repo>" merge-base --is-ancestor "<task-tip>" "release"; echo $?   # likely nonzero: squash breaks ancestry
git -C "<repo>" cherry "release" "task/completed"                          # expect '-' entries: patches already in release
git -C "<repo>" diff --stat "task/completed" "release"                     # expect empty/no content diff
```
This records that integration was a squash (ancestry check may fail; patch-id/diff checks confirm equivalence).

## 5. Preserve `review.db` outside the disposable checkout

```sh
mkdir -p "<primary-root>/review"
cp -a "case02/checkouts/completed/<db>" "<primary-root>/review/review.db"
sha256sum "<primary-root>/review/review.db"   # must match step 3
```

## 6. Protect the offline-worker registration before any pruning

```sh
git -C "<repo>" worktree list --porcelain | grep -A3 -B1 "<offline>"   # check for existing lock
git -C "<repo>" worktree lock --reason "offline share unmounted; colleague-owned, still in use" "<offline>"
git -C "<repo>" worktree list --porcelain | grep -A3 -B1 "<offline>"   # now shows 'locked ...'
```
Do **not** prune, unlock, or remove this one. A lock prevents later `worktree prune`/gc from dropping its registration.

## 7. Remove the completed checkout

```sh
git -C "<repo>" worktree remove "case02/checkouts/completed"
```
If it refuses solely because the (now preserved, checksum-verified) `review.db` remains as an ignored file, resolve that cause and retry with:
```sh
git -C "<repo>" worktree remove --force "case02/checkouts/completed"
```
No other at-risk state exists, so forcing loses nothing besides the verified copy already salvaged.

## 8. Keep the `task/completed` branch — do not delete it

```sh
git -C "<repo>" branch --list "task/completed" "release"
```
Review is still open on `task/completed`, so retain the branch. `git branch -d` would fail anyway (squash broke ancestry), and `-D` is not authorized here.

## 9. Prune only the retired scratch checkout's stale registration

```sh
git -C "<repo>" worktree prune --dry-run --verbose
```
Review **every** entry: it must list only `<scratch>`. If `<offline>` appears, stop — it means that lock did not take; fix before proceeding. Then:
```sh
git -C "<repo>" worktree prune --verbose
```

## 10. Verify the final state

```sh
git -C "<repo>" worktree list --porcelain -z
git -C "<repo>" worktree list --verbose
git -C "<repo>" branch --list "task/completed" "release"
test ! -e "case02/checkouts/completed" && echo "completed checkout removed"
ls -l "<primary-root>/review/review.db" && sha256sum "<primary-root>/review/review.db"
```

## What remains (report)

- **Branch `task/completed`**: retained; last commit integrated into `release` via squash (ancestor check non-zero, patch-id/diff checks clean); still carrying the open review. No checkout bound to it.
- **`review.db`**: preserved at `<primary-root>/review/review.db`, checksum-verified; this is the reviewer's artifact.
- **Offline-worker checkout (`<offline>`)**: registration retained and now locked with reason; directory on an unmounted, colleague-owned share — left untouched.
- **Retired scratch checkout (`<scratch>`)**: stale metadata pruned after a dry run confirmed no other entries; directory was already gone.
- **Completed checkout (`case02/checkouts/completed`)**: removed via `git worktree remove` (force only if refusal was caused solely by the preserved ignored `review.db`).
