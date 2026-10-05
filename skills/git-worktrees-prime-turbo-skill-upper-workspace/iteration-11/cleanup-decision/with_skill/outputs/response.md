Cannot verify yet — `/repo` does not exist here:

* `git -C "/repo" worktree list` -> `cannot change to '/repo'`

Walkthrough in order, per cleanup decision tree — no removal done:

1. **Still in use?** Confirm no agent/editor/terminal/service/test in `/repo/.worktrees/old-task`. Stop task-owned processes first, `cd` out. Do not clean another worker's checkout.
2. **Still needed for review?** If review can continue from merged commits, checkout may go; retain branch/ref if needed.
3. **State that disappears?** From the worktree:
   ```sh
   git -C "/repo/.worktrees/old-task" status --short --branch --untracked-files=all
   git -C "/repo/.worktrees/old-task" status --short --ignored
   git -C "/repo/.worktrees/old-task" rev-parse HEAD
   ```
   Check detached commits, unfinished ops, submodules/nested repos separately. Preserve or get authorization to discard. Squash-merged means:
   ```sh
   git -C "<repo>" merge-base --is-ancestor "<task-tip>" "<integration-ref>"
   ```
   will fail — expected, not proof of loss. Verify replacement squash commit contents instead.
4. **Safe to remove checkout?** Confirm canonical path/ownership via `git worktree list --porcelain -z`, exclude primary/current checkout/parent/siblings. Only then:
   ```sh
   git -C "<repo>" worktree remove "/repo/.worktrees/old-task"
   ```
   Never `rm -rf` the directory.
5. **Safe to delete branch?** Separate check. Requires: task-owned, unused, work verified in current `integration-ref`, or explicitly authorized abandonment. `branch -d` checks upstream, not your target — not integration evidence. If `-d` refuses due to squash history, retain until obsolete history verified safe + authorized, only then consider `-D`.
6. **Prune?** Only for intentionally removed worktrees:
   ```sh
   git -C "<repo>" worktree prune --dry-run --verbose
   git -C "<repo>" worktree prune --verbose
   ```
   Review every entry. Prune removes metadata only, not branches/dirs. Don't prune missing dirs that could be offline volumes.
7. **Verify:** `git worktree list --porcelain -z`, check path gone, branch gone/retained as decided.

To proceed I need: correct `<repo>` path, task branch name, integration ref e.g. `main`, and confirmation squash commit contains the work + no unpushed/unignored state to keep, and authorization to use `-D` if `-d` refuses.

