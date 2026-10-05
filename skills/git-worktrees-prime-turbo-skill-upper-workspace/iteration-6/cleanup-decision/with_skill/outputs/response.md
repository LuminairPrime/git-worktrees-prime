In `/repo` not verifiable here — `/repo/.worktrees/old-task` does not exist in this session — so do not remove/delete/prune yet. Walkthrough in order per cleanup decision tree:

1. **Still in use?** Confirm no agent/editor/terminal/service/test in `/repo/.worktrees/old-task`. Leave directory before removal. Do not clean another worker's checkout.
2. **Still needed for review?** If review can continue from preserved commits, checkout may go before merge; otherwise retain. Retain necessary branch/ref.
3. **State that disappears with directory?** From task checkout run:
```sh
git -C "/repo/.worktrees/old-task" status --short --branch --untracked-files=all
git -C "/repo/.worktrees/old-task" status --short --ignored
git -C "/repo/.worktrees/old-task" rev-parse HEAD
```
Check detached commits, unfinished ops, submodules/nested repos separately. Preserve or get authorization to discard. Clean status does not prove ignored files/detached commits safe.
4. **Safe to remove checkout?** Confirm canonical path + ownership:
```sh
git -C "/repo" worktree list --porcelain -z
```
Exclude primary checkout, current cwd, parent, sibling tasks. Run from surviving checkout/bare repo only:
```sh
git -C "/repo" worktree remove "/repo/.worktrees/old-task"
```
Do not `rm -rf` directory. Removing checkout leaves branch.
5. **Safe to delete branch?** Squash breaks ancestry — expect this to fail:
```sh
git -C "/repo" merge-base --is-ancestor "<task-tip>" "<integration-ref>"
```
`branch -d` checks upstream, not intended target; success is not integration evidence. Verify replacement commits + resulting diff vs current integration ref. Retain branch for pending review; closed PR alone insufficient. Only if verified integrated/preserved elsewhere or explicitly authorized for abandonment:
```sh
git -C "/repo" branch -d "<task-branch>"
```
If refuses due to squash history, retain until obsolete history verified safe + authorized, only then consider `branch -D`.
6. **Prune?** Prune removes stale metadata only, not branches/directories:
```sh
git -C "/repo" worktree prune --dry-run --verbose
```
Proceed to `git -C "/repo" worktree prune --verbose` only if every entry is intentionally removed. Missing dir may be offline volume — do not prune/unlock.
7. **Verify:**
```sh
git -C "/repo" worktree list --porcelain -z
```
Check path gone, chosen refs gone. Report retained items + why.

Provide: task-branch name, integration ref, `HEAD`, and outputs above to authorize 4-6.
