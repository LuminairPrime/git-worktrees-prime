Cannot approve removal yet — `/repo/.worktrees/old-task` not found from here:

* `/repo` does not exist; `git -C /repo worktree list` fails.
* Current checkout: `/tmp/skill-up-2505016780` (only `.opencode/`), not a git repo.

Walkthrough in order, per cleanup decision tree — run from surviving checkout (`/repo` or primary root):

1. **In use?** Leave directory, stop task-owned processes/services/tests/editors. Do not clean another worker's checkout. Retain if still in use.
2. **Needed for review?** If review needs this checkout, retain. Checkout may go before merge only if review can continue from preserved commits.
3. **State would disappear?** In `/repo/.worktrees/old-task`:
```sh
git -C "/repo/.worktrees/old-task" status --short --branch --untracked-files=all
git -C "/repo/.worktrees/old-task" status --short --ignored
git -C "/repo/.worktrees/old-task" rev-parse HEAD
```
Check unfinished ops, detached commits, submodules/nested repos separately. Preserve or authorize discard. Reproducible products need no backup.
4. **Safe to remove checkout?** Confirm canonical path + ownership:
```sh
git -C "/repo" worktree list --porcelain -z
```
Must be exactly `/repo/.worktrees/old-task`, not primary, cwd, parent, or sibling task. Then only:
```sh
git -C "/repo" worktree remove "/repo/.worktrees/old-task"
```
Do not `rm -rf`.
5. **Safe to delete branch?** Squash-merge breaks ancestry, so `branch -d` likely refuses and `merge-base --is-ancestor` will fail:
```sh
git -C "/repo" rev-parse HEAD
git -C "/repo" merge-base --is-ancestor "<task-tip>" "<integration-ref>"
```
`branch -d` checks upstream, not target — success is not integration evidence. Verify replacement squash commit contents/diff against intended target. Retain if pending review; closed PR alone insufficient. Only if verified integrated/preserved or explicitly authorized for abandonment:
```sh
git -C "/repo" branch -d "<task-branch>"
```
If refused, retain until obsolete history verified safe + authorized, only then consider `branch -D`.
6. **Prune?** Only for intentionally removed worktrees:
```sh
git -C "/repo" worktree prune --dry-run --verbose
```
Review every entry — missing dir may be offline volume. Then, with same expiry:
```sh
git -C "/repo" worktree prune --verbose
```
Prune removes metadata only, not branches/directories.
7. **Verify:**
```sh
git -C "/repo" worktree list --porcelain -z
```

Provide: task-branch name, integration target + squash commit, output of 3-4, and authorization to discard state / `-D` if needed, and I can re-evaluate.

