In order, from a surviving checkout (`<primary-root>`, not `case02/checkouts/completed`):

1. Inventory, resolve canonical paths/ownership:
```sh
git -C "<primary-root>" worktree list --porcelain -z
```
Confirm: exact absolute path for `case02/checkouts/completed` -> `task/completed`, `release` integration target, colleague-owned offline-worker path (unmounted, in use), deleted scratch path. Do not remove primary, cwd, parent, or siblings.

2. Inspect disposable state in completed checkout — `references/raw-git-commands.md:46-48`:
```sh
git -C "case02/checkouts/completed" status --short --branch --untracked-files=all
git -C "case02/checkouts/completed" status --short --ignored
git -C "case02/checkouts/completed" rev-parse HEAD
```
Check: tracked/untracked diffs, `review.db` ignored file, detached commits, `MERGE_HEAD/REBASE_HEAD/CHERRY_PICK_HEAD`, submodules/nested repos separately.

3. Preserve reviewer state outside deletion path (`remove` deletes ignored files):
```sh
ls -l "case02/checkouts/completed/review.db"
cp "case02/checkouts/completed/review.db" "<safe-path-outside-case02/checkouts/completed>/review.db"
ls -l "<safe-path-outside-case02/checkouts/completed>/review.db"
```

4. Verify squash-integration; expect ancestry break — `references/raw-git-commands.md:51`:
```sh
git -C "<primary-root>" merge-base --is-ancestor "$(git -C "case02/checkouts/completed" rev-parse HEAD)" "release"; echo $?
```
`exit 1` expected for squash. Verify replacement instead: inspect `release` log and resulting tree/diff for `task/completed` changes. `branch -d` success is not evidence here.

5. Leave directory, remove only exact checkout — `references/raw-git-commands.md:55`:
```sh
cd "<primary-root>"
git -C "<primary-root>" worktree remove "<abs-path-to-case02/checkouts/completed>"
```
No `rm -rf`, no `--force`, no colleague checkout.

6. Verify removal:
```sh
git -C "<primary-root>" worktree list --porcelain -z
test ! -e "<abs-path-to-case02/checkouts/completed>" && echo "removed"
```

7. Branch decision: retain. Do NOT run:
```sh
git -C "<primary-root>" branch -d "task/completed"
```
Reason: open review on `task/completed` needs the ref; squash breaks `-d` ancestry check.

8. Stale registrations, dry-run first — `references/raw-git-commands.md:61-62`:
```sh
git -C "<primary-root>" worktree prune --dry-run --verbose
```
Prune only if every entry is the intentionally deleted retired scratch. Unmounted offline-worker missing ≠ deletable. If dry-run lists offline-worker, do NOT prune. If only scratch:
```sh
git -C "<primary-root>" worktree prune --verbose
git -C "<primary-root>" worktree list --porcelain -z
```

Remains to report:
- Removed: checkout `case02/checkouts/completed`.
- Retained: branch `task/completed` (open review, squash-integrated to `release`); preserved `review.db` at `<safe-path>/review.db`; registration for colleague-owned offline-worker checkout (unmounted, still in use, never pruned/unlocked); primary checkout.
- Pruned (conditional): stale registration for retired scratch checkout already deleted from disk — only if dry-run proved no offline entry.

