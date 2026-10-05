Cannot proceed — verification failed:

* `/repo` does not exist, `git -C "/repo" worktree list` fails.
* `/repo/.worktrees/old-task` not found.
* Task branch name and integration target ref not provided.

No removal, branch deletion, or prune performed.

Ordered checks required per cleanup decision tree, with raw Git commands:

1. **In use?** Leave checkout, confirm `pwd` is not inside `/repo/.worktrees/old-task`, no agent/editor/terminal/service/test owns it. Stop task-owned processes only.
2. **Still needed for review?** You state squash-merged and done — if review can continue from integration commit, checkout may go; retain branch/ref if needed.
3. **Disappearing state?** From task checkout:
   ```sh
   git -C "<worktree>" status --short --branch --untracked-files=all
   git -C "<worktree>" status --short --ignored
   git -C "<worktree>" rev-parse HEAD
   ```
   Check submodules/nested repos, detached commits, rebase/merge/bisect in progress. Preserve or authorize discard.
4. **Safe to remove checkout?** Confirm canonical path vs inventory:
   ```sh
   git -C "<repo>" worktree list --porcelain -z
   ```
   Must be exact task checkout, not primary, current dir, parent, or sibling task. Then only:
   ```sh
   git -C "<repo>" worktree remove "/repo/.worktrees/old-task"
   ```
   Never `rm -rf` the directory.
5. **Safe to delete branch?** Separate decision. Squash breaks ancestry, so:
   ```sh
   git -C "<repo>" merge-base --is-ancestor "<task-tip>" "<integration-ref>"
   ```
   will exit non-zero — expected, not proof of loss. Verify replacement by diff/patch-id against integration target, confirm branch is task-owned, unused elsewhere, no pending PR. Then only:
   ```sh
   git -C "<repo>" branch -d "<task-branch>"
   ```
   If refused, retain. Use `-D` only after obsolete history is verified safe with explicit authorization.
6. **Prune?** Only for intentionally removed registrations, after reviewing all entries:
   ```sh
   git -C "<repo>" worktree prune --dry-run --verbose
   git -C "<repo>" worktree prune --verbose
   ```
   Do not prune offline volumes; prune removes metadata, not branches/directories. Keep expiry flags identical.
7. **Verify:**
   ```sh
   git -C "<repo>" worktree list --porcelain -z
   ```
   Check path gone, branch status, report retained items.

Provide: correct `<repo>` path, `<task-branch>`, and `<integration-ref>` to run 3-6.
