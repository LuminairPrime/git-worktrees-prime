At `/repo/.worktrees/old-task` — checkout removal and branch deletion are separate. `/repo` not present in this environment, so verified here, run from a surviving checkout:

1. **Still in use?** Leave the worktree dir, stop task-owned processes/services/tests/editors/terminals. Do not clean another worker's checkout.
2. **Still needed for review?** If review can continue from the squash commit, checkout can go; retain branch until step 5 passes.
3. **State would disappear?** Squash-merge does not preserve this:
```sh
git -C "/repo/.worktrees/old-task" status --short --branch --untracked-files=all
git -C "/repo/.worktrees/old-task" status --short --ignored
git -C "/repo/.worktrees/old-task" rev-parse HEAD
```
Check detached commits, unfinished merges/rebase/bisect, submodules separately. Backup or authorize discard. Do not `rm -rf`; use `worktree remove`.

4. **Safe to remove checkout?** Confirm canonical path/ownership:
```sh
git -C /repo worktree list --porcelain -z
```
Must not be primary, cwd, parent, or sibling task. Then only if 1-3 permit:
```sh
git -C /repo worktree remove "/repo/.worktrees/old-task"
```

5. **Safe to delete branch?** This is the squash case — ancestry is broken, `branch -d` is not evidence:
```sh
git -C /repo merge-base --is-ancestor "<task-tip>" "<integration-ref>"
```
Expect failure for squash. Instead verify replacement: diff task-tip vs integration ref contains the work, `log` shows squash commit in intended target after fresh fetch. Closed PR alone insufficient. Only delete unused, task-owned branch with verified integration/preserved ref/explicit abandon authorization. Then:
```sh
git -C /repo branch -d "<task-branch>"
```
If refuses, retain branch until obsolete history verified safe + authorized for `-D`.

6. **Prune?** Prune removes registrations only, not dirs/branches. Review every entry:
```sh
git -C /repo worktree prune --dry-run --verbose
git -C /repo worktree prune --verbose
```
Same expiry both runs. Do not prune offline volumes.

7. **Verify:**
```sh
git -C /repo worktree list --porcelain -z
```
Confirm path gone, branch gone/retained, report retained + why.

To proceed I need: exact `<task-branch>`, `<integration-ref>` e.g. `main`, and confirmation of 1-3 — no active use, no uncommitted/untracked/ignored value to keep, squash commit hash verified in target.

