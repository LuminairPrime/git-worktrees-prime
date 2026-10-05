Checked out `task/completed` at `case02/checkouts/completed` is integrated, not active development. Target: `release`. Owner: this task for `completed` only.

Would run, in order, from main checkout, not from checkout to be deleted:

1. Establish inventory, do not act on guess:
```sh
pwd
git rev-parse --absolute-git-common-dir
git worktree list --porcelain -z | tr '\0' '\n'
git worktree list --porcelain -v
```
Check: canonical absolute path for `case02/checkouts/completed`, its branch `task/completed`, its `HEAD`, registration vs manager inventory.

2. Inspect completed checkout state:
```sh
git -C "<primary-root>/case02/checkouts/completed" rev-parse --show-toplevel
git -C "<primary-root>/case02/checkouts/completed" rev-parse --abbrev-ref HEAD
git -C "<primary-root>/case02/checkouts/completed" rev-parse HEAD
git -C "<primary-root>/case02/checkouts/completed" status --porcelain=v1 -uall --ignored -z | tr '\0' '\n'
git -C "<primary-root>/case02/checkouts/completed" stash list
git -C "<primary-root>/case02/checkouts/completed" log --oneline -5
```
Check unfinished `rebase/merge/cherry-pick`, submodules/nested repos separately. Do not `pull`, `reset`, `clean`, `rm -rf`.

3. Verify squash-integration into current `release`, ancestry will not match:
```sh
git fetch origin release --prune
git rev-parse --verify refs/heads/task/completed
git rev-parse --verify refs/heads/release
git log --oneline -5 release
git diff task/completed release --stat
git cherry release task/completed -v
```
Check: `diff task/completed release` empty for task paths = replacement commits carry the work. `branch -d` success is not evidence, not used here.

4. Preserve ignored state reviewer needs, outside deletion path:
```sh
git -C "<primary-root>/case02/checkouts/completed" check-ignore -v review.db
ls -l "<primary-root>/case02/checkouts/completed/review.db"
sha256sum "<primary-root>/case02/checkouts/completed/review.db"
cp -a "<primary-root>/case02/checkouts/completed/review.db" "<safe-outside-path>/review.db.task-completed-<HEAD-short>.db"
sha256sum "<safe-outside-path>/review.db.task-completed-<HEAD-short>.db"
ls -l "<safe-outside-path>/review.db.task-completed-<HEAD-short>.db"
```
Do not bulk-copy dependencies/build outputs.

5. Leave directory, remove only exact checkout via Git:
```sh
cd "<primary-root>"
git worktree remove "<primary-root>/case02/checkouts/completed"
```
No `--force` - already verified clean/preserved. No filesystem `rm`, no parent/sibling removal, no current-dir removal.

6. Evaluate branch: explicitly retain:
```sh
git branch --list "task/completed"
git log --oneline -3 task/completed
```
Do NOT run `git branch -d/-D task/completed`. Reason: review remains open on `task/completed`. Checkout may go before merge, branch/ref must stay.

7. Evaluate stale registrations, dry-run only with same expiry:
```sh
git worktree prune -n -v
git worktree list --porcelain -v
```
Check: dry-run will list `scratch` - intentionally deleted from disk, prunable - and `offline-worker` - unmounted share, colleague-owned, still in use, appears missing but is not deleted. Per rule: missing dir may be offline volume, prune only if every entry is intentional. Condition fails.
Do NOT run `git worktree prune`, `git worktree unlock`, `git gc`, do NOT delete `<git-common-dir>/worktrees/<id>` by hand.

8. Verify result:
```sh
git worktree list --porcelain -z | tr '\0' '\n'
test ! -e "<primary-root>/case02/checkouts/completed" && echo "completed path gone"
git rev-parse --verify refs/heads/task/completed
git rev-parse --verify refs/heads/release
ls -l "<safe-outside-path>/review.db.task-completed-<HEAD-short>.db"
```

Report what remains:

* Removed: linked checkout `<primary-root>/case02/checkouts/completed` only.
* Retained branch `refs/heads/task/completed` at same `HEAD`: needed for open review, squash ancestry broken so integration verified by diff, not by `branch -d`.
* Preserved: `review.db` copy at `<safe-outside-path>/review.db.task-completed-<HEAD-short>.db` with verified checksum; original died with checkout.
* Retained untouched: `offline-worker` registration/path on unmounted colleague-owned share, still in use.
* Retained stale: `scratch` registration for already-deleted disk path; blanket `prune` withheld to avoid destroying `offline-worker` registration. Re-prune only when share remounted and dry-run shows only intentional deletions.

