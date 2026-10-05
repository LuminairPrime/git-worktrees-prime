No removal done — `/repo/.worktrees/old-task` is not reachable from this session (`/repo: No such file or directory`, cwd `/tmp/skill-up-48818318` is not a git repo). Run the checks below from the primary checkout before removing anything.

Walkthrough in order, for `<worktree>=/repo/.worktrees/old-task`:

1. **Still in use?** Retain if any agent/editor/terminal/service/test owns it. `cd` out of `<worktree>` before removal. Do not clean another worker's checkout.
2. **Still needed for review?** Checkout may go if review can continue from preserved commits; otherwise retain. Retain the branch if review is pending.
3. **State that disappears with the directory?** From the task checkout:
```sh
git -C "/repo/.worktrees/old-task" status --short --branch --untracked-files=all
git -C "/repo/.worktrees/old-task" status --short --ignored
git -C "/repo/.worktrees/old-task" rev-parse HEAD
```
Check detached commits, `MERGE_HEAD/CHERRY_PICK_HEAD/REBASE_HEAD`, submodules/nested repos separately. Preserve or authorize discard. Clean status does not prove ignored files/detached commits are preserved.
4. **Safe to remove checkout?** Confirm canonical path and ownership:
```sh
git -C "/repo" worktree list --porcelain -z
```
Must be exactly `/repo/.worktrees/old-task`, not primary, cwd, parent, or sibling task. Then, from a surviving checkout:
```sh
git -C "/repo" worktree remove "/repo/.worktrees/old-task"
```
Do not `rm -rf` the directory.
5. **Safe to delete branch?** Squash-merge special case: ancestry is broken, so this will likely fail:
```sh
git -C "/repo" merge-base --is-ancestor "<task-tip>" "<integration-ref>"
```
`branch -d` success is not integration evidence; a closed PR alone is insufficient. Manually verify replacement commits and resulting diff vs current `integration-ref` (fetch first). Only if verified integrated/preserved elsewhere/authorized for abandonment:
```sh
git -C "/repo" branch -d "<task-branch>"
```
If it refuses, retain. Only use `-D` after obsolete history is verified safe and deletion is authorized.
6. **Prune stale metadata?** Only for intentionally removed worktrees, after reviewing every entry. Missing dir could be offline volume — do not prune that case:
```sh
git -C "/repo" worktree prune --dry-run --verbose
git -C "/repo" worktree prune --verbose
```
Same expiry options for dry-run and real run. Prune removes registrations only, not branches/directories.
7. **Verify:**
```sh
git -C "/repo" worktree list --porcelain -z
```
Confirm path gone, branch disposition, report anything retained and why.

Provide `<task-branch>` and `<integration-ref>` + current `worktree list` output to authorize steps 4-6.
