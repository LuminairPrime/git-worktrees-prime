Completed `task/completed` checkout reclaim — squash case, open review, mixed stale registrations:

Do not `rm -rf`, do not `branch -D`, do not `prune`.

1. Inventory, from surviving main checkout:
```sh
git -C "<primary-root>" worktree list --porcelain -z
git -C "<primary-root>" rev-parse --verify "release^{commit}"
git -C "<primary-root>" rev-parse --verify "task/completed^{commit}"
```
Check: canonical absolute path for `case02/checkouts/completed`, owner `task/completed`, plus `offline-worker` missing/unmounted colleague-owned, `scratch` missing/deleted.

2. Inspect disposable state in target only `references/raw-git-commands.md:45-48`:
```sh
git -C "<abs-path>/case02/checkouts/completed" status --short --branch --untracked-files=all
git -C "<abs-path>/case02/checkouts/completed" status --short --ignored
git -C "<abs-path>/case02/checkouts/completed" rev-parse HEAD
ls -la "<abs-path>/case02/checkouts/completed/review.db"
```
Check: tracked clean, `review.db` present as ignored, no unfinished `MERGE_HEAD/REBASE_HEAD/CHERRY_PICK_HEAD`, no detached valuable commits, no submodules.

3. Verify integration — expect ancestry failure for squash:
```sh
git -C "<primary-root>" merge-base --is-ancestor "task/completed" "release"; echo $?
git -C "<primary-root>" diff "release" "task/completed" --stat
git -C "<primary-root>" log --oneline "release" -5
```
Check: exit non-zero is expected, `diff` shows no unique `task/completed` changes; squash commit on `release` verified.

4. Preserve needed ignored state outside deletion path before removal:
```sh
cp "<abs-path>/case02/checkouts/completed/review.db" "<abs-path>/case02/preserved/completed-review.db"
ls -la "<abs-path>/case02/preserved/completed-review.db"
```
Do not rely on harness archive; ignored files do not follow.

5. Leave directory, remove only exact checkout `references/raw-git-commands.md:55`:
```sh
cd "<primary-root>"
git -C "<primary-root>" worktree remove "<abs-path>/case02/checkouts/completed"
test ! -e "<abs-path>/case02/checkouts/completed" && echo "removed"
git -C "<primary-root>" worktree list --porcelain -z
```

6. Retain branch — do not delete:
```sh
git -C "<primary-root>" branch -vv --list "task/completed"
```
Reason: review open on `task/completed`; closed/integrated squash alone is insufficient, `branch -d` checks upstream not `release` and must refuse on squash-diverged history. No `-D`.

7. Stale metadata — dry-run then abort:
```sh
git -C "<primary-root>" worktree prune --dry-run --verbose
```
Check: lists `scratch` intentionally deleted + `offline-worker` unmounted/still-in-use. Per decision tree: prune only if every entry is intentionally removed. Do NOT run `worktree prune --verbose`, do not `unlock` offline volume.

8. Final verify:
```sh
git -C "<primary-root>" worktree list --porcelain -z
git -C "<primary-root>" branch --list "task/completed" "release"
```

Remains:
* Removed: `<abs-path>/case02/checkouts/completed` directory gone.
* Preserved: `review.db` copied to `<abs-path>/case02/preserved/completed-review.db` for reviewer.
* Retained branch `task/completed` for open review; integrated squash lives on `release`.
* Retained registration `offline-worker` — colleague-owned, unmounted, still in use.
* Temporarily retained stale registration `scratch` — path already deleted, cannot prune safely until `offline-worker` remounts and dry-run is clean.

