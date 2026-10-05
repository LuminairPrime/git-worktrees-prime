At `/repo/.worktrees/old-task` I can't verify — `/repo` doesn't exist here — so don't remove yet. Walkthrough in order, per cleanup decision tree:

**1. Still in use?**
Leave that directory, stop task-owned processes/services/tests. Don't clean another worker's checkout.

**2. Still needed for review?**
If review can continue from merged commits, checkout may go; otherwise retain.

**3. Would state disappear?**
From the worktree, check:
```sh
git -C "/repo/.worktrees/old-task" status --short --branch --untracked-files=all
git -C "/repo/.worktrees/old-task" status --short --ignored
git -C "/repo/.worktrees/old-task" rev-parse HEAD
```
Also check unfinished ops, submodules/nested repos, detached commits. Preserve or authorize discard. Reproducible builds need no backup.

**4. Safe to remove checkout?**
Confirm canonical path + ownership first:
```sh
git -C "/repo" worktree list --porcelain -z
```
Must not be primary, cwd, parent, or sibling task. Then only:
```sh
git -C "/repo" worktree remove "/repo/.worktrees/old-task"
```
Don't `rm -rf` the directory.

**5. Safe to delete branch?**
Separate from checkout removal. Since squash breaks ancestry:
- `merge-base --is-ancestor <task-tip> <integration-ref>` will likely fail — expected, not proof of loss.
- `branch -d` checks upstream, not your integration target — success is not integration evidence.

Verify with current target ref:
```sh
git -C "/repo" rev-parse HEAD
git -C "/repo" merge-base --is-ancestor "<task-tip>" "<integration-ref>"
git -C "/repo" branch -d "<task-branch>"
```
If `-d` refuses, retain branch until obsolete history is verified safe + authorized, only then consider `-D`. Name branch/ref separately from checkout path.

**6. Prune?**
Prune removes stale registrations only, not branches/dirs:
```sh
git -C "/repo" worktree prune --dry-run --verbose
git -C "/repo" worktree prune --verbose
```
Prune only if every dry-run entry is intentionally removed. Don't prune missing dirs that could be offline volumes.

**7. Verify:**
```sh
git -C "/repo" worktree list --porcelain -z
```
Check path gone, intended refs gone/retained as decided.

Provide `<task-branch>`, `<task-tip>`, and `<integration-ref>` if you want the squash verification checked.
