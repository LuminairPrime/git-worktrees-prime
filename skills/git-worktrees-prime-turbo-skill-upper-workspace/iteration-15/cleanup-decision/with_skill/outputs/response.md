Cannot remove yet — verification failed at step 0:

* `/repo/.worktrees/old-task` and `/repo` do not exist from current checkout `/tmp/skill-up-1378530662`. No removal, branch delete, or prune executed.

Walk through in order per cleanup decision tree before any `raw-git` cleanup:

1. **Still in use?** Confirm no agent/editor/terminal/service/test in `/repo/.worktrees/old-task`. `leave` directory before removal. Do not clean another worker's checkout.
2. **Still needed for review?** If review can continue from preserved commits, checkout may go; retain branch/ref if needed.
3. **State loss?** From task checkout, check:
   ```sh
   git -C "/repo/.worktrees/old-task" status --short --branch --untracked-files=all
   git -C "/repo/.worktrees/old-task" status --short --ignored
   git -C "/repo/.worktrees/old-task" rev-parse HEAD
   ```
   Preserve tracked/untracked/ignored, detached commits, unfinished ops, submodules. Clean status does not prove ignored/detached safe.
4. **Safe to remove checkout?** Confirm canonical path/ownership via:
   ```sh
   git -C "/repo" worktree list --porcelain -z
   ```
   Remove only exact task checkout via manager or:
   ```sh
   git -C "/repo" worktree remove "/repo/.worktrees/old-task"
   ```
   Exclude: primary checkout, current WD, parent dir, sibling tasks. Never `rm -rf` directory.
5. **Safe to delete branch?** Squash breaks ancestry — `branch -d` success is not integration proof, and refusal is expected. Verify replacement commits, not ancestry:
   ```sh
   git -C "/repo" merge-base --is-ancestor "<task-tip>" "<integration-ref>"
   # + diff/changes review against current integration ref
   git -C "/repo" branch -d "<task-branch>"
   ```
   Delete only if unused, task-owned, and verified integrated/preserved or explicitly authorized for abandonment. Closed PR alone insufficient. If ` -d` refuses, retain until authorized; only then consider `-D`.
6. **Stale metadata?** Only for intentionally removed worktrees, after reviewing every entry:
   ```sh
   git -C "/repo" worktree prune --dry-run --verbose
   git -C "/repo" worktree prune --verbose
   ```
   Same expiry options. Prune removes registrations only, not branches/directories. Missing dir may be offline volume — do not prune/unlock.
7. **Verify:**
   ```sh
   git -C "/repo" worktree list --porcelain -z
   # + check removed path gone, intended refs gone/retained as decided
   ```

Provide to proceed: correct `<repo>` absolute path, `<task-branch>` name, and verified `<integration-ref>` squash landed in, plus confirmation of 1-3.
