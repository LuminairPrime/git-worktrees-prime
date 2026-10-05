Cannot authorize removal yet — verification failed at step 4:

`/repo/.worktrees/old-task` does not resolve: `/repo` does not exist in this environment.

Walkthrough per cleanup decision tree — do in order, stop on blocker:

1. **Still in use?** Leave `/repo/.worktrees/old-task` before removal, stop only task-owned processes/services/tests. Confirm no other agent/editor/terminal owns it. Do not clean another worker's checkout.

2. **Still needed for review?** You state done + squash-merged. If review can continue from integration commits, checkout may go; retain branch until step 5 passes.

3. **State that disappears with directory?** From the worktree itself:
```sh
git -C "/repo/.worktrees/old-task" status --short --branch --untracked-files=all
git -C "/repo/.worktrees/old-task" status --short --ignored
git -C "/repo/.worktrees/old-task" rev-parse HEAD
```
Check detached commits, unfinished rebase/merge/bisect, submodules/nested repos separately. Preserve or authorize discard. Clean status alone does not preserve ignored files.

4. **Safe to remove checkout?** Requires:
```sh
git -C "/repo" worktree list --porcelain -z
```
Confirm canonical absolute path and ownership, exclude primary checkout, current cwd, parent dir, sibling tasks. Then only:
```sh
git -C "/repo" worktree remove "/repo/.worktrees/old-task"
```
Blocked: cannot confirm against `worktree list`. Do not delete via filesystem.

5. **Safe to delete branch?** Need exact `<task-branch>` and `<integration-ref>` — you did not name them. Squash breaks ancestry, so:
```sh
git -C "/repo" merge-base --is-ancestor "<task-tip>" "<integration-ref>"
git -C "/repo" branch -d "<task-branch>"
```
will likely fail/refuse — that is not integration evidence. Must verify replacement squash commit contains the changes, branch is unused/task-owned, and no pending review needs it. Only then consider `-D` with explicit authorization.

6. **Prune?** Only for intentionally removed worktrees, after reviewing every entry:
```sh
git -C "/repo" worktree prune --dry-run --verbose
git -C "/repo" worktree prune --verbose
```
Do not prune offline volumes.

7. **Verify:**
```sh
git -C "/repo" worktree list --porcelain -z
```

Provide `<task-branch>`, `<integration-ref>`/squash commit, and correct repo path if `/repo` is wrong, then I can run steps 3-4 checks.

