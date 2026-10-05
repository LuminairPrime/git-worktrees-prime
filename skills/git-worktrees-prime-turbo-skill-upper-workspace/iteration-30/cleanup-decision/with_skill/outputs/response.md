In this environment `/repo` does not exist and `/tmp/skill-up-3277420849` is not a git repo, so no removal/deletion/prune was performed. Walkthrough for `/repo/.worktrees/old-task` in order, per cleanup decision tree:

Checkout path ` /repo/.worktrees/old-task` and branch are separate — removing checkout leaves branch. Provide branch name and integration target ref to proceed.

1. **Still in use?** Retain if any agent, editor, terminal, service, test still uses it. Stop only task-owned processes; `cd` out before removal. Do not clean another worker's checkout.
2. **Still needed for review/dev?** If review can continue from integrated commits, checkout may go; otherwise retain.
3. **State that disappears with directory?** From task checkout, run:
```sh
git -C "/repo/.worktrees/old-task" status --short --branch --untracked-files=all
git -C "/repo/.worktrees/old-task" status --short --ignored
git -C "/repo/.worktrees/old-task" rev-parse HEAD
```
Check detached commits, unfinished ops, submodules/nested repos separately. Preserve or authorize discard. Clean status alone does not preserve ignored files.
4. **Safe to remove checkout?** Confirm canonical path/ownership against:
```sh
git -C "<repo>" worktree list --porcelain -z
```
Never remove primary, current working dir, parent, or sibling task. Only via manager or:
```sh
git -C "<repo>" worktree remove "/repo/.worktrees/old-task"
```
No filesystem `rm`.
5. **Safe to delete branch?** Squash breaks ancestry, so `branch -d` is not evidence and will likely refuse. Verify replacement manually:
```sh
git -C "<repo>" merge-base --is-ancestor "<task-tip>" "<integration-ref>"
# for squash: diff task-tip vs integration result, verify squash commit contents
git -C "<repo>" branch -d "<task-branch>"
```
Delete only task-owned, unused branch with verified integration into current target, preserved under another ref, or explicit abandon authorization. Retain if pending review. Closed PR alone insufficient. If `-d` refuses, retain until obsolete history verified safe/authorized, only then consider `-D`.
6. **Prune?** Prune removes stale registrations only, not branches/dirs:
```sh
git -C "<repo>" worktree prune --dry-run --verbose
git -C "<repo>" worktree prune --verbose
```
Prune only if every dry-run entry is intentionally removed. Missing dir may be offline volume — do not prune/unlock.
7. **Verify:**
```sh
git -C "<repo>" worktree list --porcelain -z
```
Check path gone, refs as intended. Report retained items.

Provide outputs of 3-5 plus branch name and integration ref for approval.

