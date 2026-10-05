Cannot verify `/repo/.worktrees/old-task` here: `/repo` does not exist in this environment.

Walkthrough in required order, per cleanup decision tree:

1. **In use?** Confirm no agent/editor/terminal/service/test in that path. `cd` out before removal. Do not clean another worker's checkout.
2. **Needed for review?** If review can continue from merged commits, checkout may go; retain branch until step 5 passes.
3. **State loss?** From `references/raw-git-commands.md:46-48`:
   ```sh
   git -C "/repo/.worktrees/old-task" status --short --branch --untracked-files=all
   git -C "/repo/.worktrees/old-task" status --short --ignored
   git -C "/repo/.worktrees/old-task" rev-parse HEAD
   ```
   Check detached commits, submodules/nested repos separately. Preserve or authorize discard.
4. **Remove checkout?** Confirm canonical path/ownership:
   ```sh
   git -C "/repo" worktree list --porcelain -z
   ```
   Exclude primary, cwd, parent, siblings. Only then, from surviving checkout:
   ```sh
   git -C "<repo>" worktree remove "/repo/.worktrees/old-task"
   ```
   Never `rm -rf` the directory.
5. **Delete branch?** Squash-merge breaks ancestry, so:
   - `branch -d` checks upstream, not target — success is not proof.
   - `git -C "<repo>" merge-base --is-ancestor "<task-tip>" "<integration-ref>"` will exit non-zero for squash; needs review.
   - Verify replacement commits + resulting diff against current `integration-ref` (fetch first). Retain for pending review; closed PR alone insufficient.
   - Only if verified integrated/preserved/authorized: `git -C "<repo>" branch -d "<task-branch>"`. If refuses, retain until obsolete history verified safe/authorized, then consider `-D`.
6. **Prune?** Only stale registrations from intentionally removed worktrees:
   ```sh
   git -C "/repo" worktree prune --dry-run --verbose
   git -C "/repo" worktree prune --verbose
   ```
   Review every dry-run entry. Missing dir may be offline volume — do not prune/unlock.
7. **Verify:** `worktree list --porcelain -z`, check path gone, branch state. Report retained items + why.

Provide actual `<task-branch>`, `<integration-ref>`, and `task-tip` SHA + `status` output to authorize `remove` / `-d` / `prune`.

