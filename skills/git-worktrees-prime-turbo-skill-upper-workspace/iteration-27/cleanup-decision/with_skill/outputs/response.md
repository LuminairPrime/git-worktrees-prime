Cannot proceed yet — `/repo` does not exist here:

* `ls -ld /repo /repo/.worktrees/old-task` -> `No such file or directory`
* `git -C "/repo" worktree list` -> `cannot change to '/repo'`

Walkthrough in cleanup decision-tree order for `<repo>=/repo`, `<worktree>=/repo/.worktrees/old-task`:

1. **Still in use?** Stop task processes, leave the directory. Do not remove another worker's checkout or the current working directory.
2. **Still needed for review?** You state merged — if review can continue from target commits, checkout may go before branch deletion; retain branch until step 5 passes.
3. **State that would disappear?** From a surviving checkout:
   ```sh
   git -C "/repo/.worktrees/old-task" status --short --branch --untracked-files=all
   git -C "/repo/.worktrees/old-task" status --short --ignored
   git -C "/repo/.worktrees/old-task" rev-parse HEAD
   ```
   Check detached commits, `MERGE_HEAD/CHERRY_PICK_HEAD/REBASE_HEAD` unfinished ops, submodules/nested repos separately. Preserve or get authorization to discard.
4. **Safe to remove checkout?** Confirm canonical path/ownership first:
   ```sh
   git -C "/repo" worktree list --porcelain -z
   ```
   Exclude primary, current directory, parent, sibling tasks. Then only:
   ```sh
   git -C "/repo" worktree remove "/repo/.worktrees/old-task"
   ```
   Never `rm -rf` the directory.
5. **Safe to delete branch?** Squash breaks ancestry, so this needs manual verification:
   ```sh
   git -C "/repo" merge-base --is-ancestor "<task-tip>" "<integration-ref>"
   ```
   Expect failure for squash — not proof of loss. Compare replacement commits and resulting diff against current `<integration-ref>`. `branch -d` checks upstream, not your target, so success is not integration evidence. If it refuses, retain the branch; only use `branch -D` with explicit authorization after obsolete history is verified safe. You did not name `<task-branch>` or `<integration-ref>` — provide both.
6. **Prune?** Only stale registrations, never branches/directories:
   ```sh
   git -C "/repo" worktree prune --dry-run --verbose
   git -C "/repo" worktree prune --verbose
   ```
   Prune only if every dry-run entry is intentionally removed. Do not prune a missing directory that may be offline volume.
7. **Verify:**
   ```sh
   git -C "/repo" worktree list --porcelain -z
   git -C "/repo" branch --list "<task-branch>"
   ```

Provide task-branch name and integration ref, and run from a host where `/repo` exists to continue at step 3.

