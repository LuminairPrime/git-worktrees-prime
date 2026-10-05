Cannot remove/delete/prune yet — verification blocked:

Checked: `/repo/.worktrees/old-task` does not exist (`No such file or directory`), and `/tmp/skill-up-3596117615` is not a git repo. No branch name, integration target, or HEAD provided.

Walkthrough per cleanup decision tree, in order:

1. **Still in use?** Unverified. Confirm no agent/editor/terminal/service/test owns `/repo/.worktrees/old-task`. Leave directory before removal.
2. **Still needed for review?** You state squash-merged and done — if review can continue from preserved commits, checkout may go, retain branch until step 5 passes.
3. **State would disappear?** Blocked. Requires from task checkout:
   `git -C "<worktree>" status --short --branch --untracked-files=all`
   `git -C "<worktree>" status --short --ignored`
   `git -C "<worktree>" rev-parse HEAD`
   Plus check detached commits, unfinished ops, submodules. Cannot run — path missing.
4. **Safe to remove checkout?** Blocked. Requires `git worktree list --porcelain -z` to confirm canonical path/ownership, and exclude primary checkout, cwd, parent, siblings. Then only: `git -C "<repo>" worktree remove "<worktree>"`. Never delete via filesystem.
5. **Safe to delete branch?** Blocked. Branch name unknown. Requires verifying tip vs current integration ref:
   `git -C "<repo>" merge-base --is-ancestor "<task-tip>" "<integration-ref>"`
   For squash-merge ancestry will fail — expected. Must verify replacement commits/changes instead. `branch -d` may refuse; only use `-D` with explicit authorization after that verification. Closed PR alone is insufficient.
6. **Prune stale metadata?** Blocked. Requires:
   `git -C "<repo>" worktree prune --dry-run --verbose`
   then `prune --verbose` with same options, only if every entry is an intentionally removed worktree. Don't prune offline volumes.
7. **Verify result:** `git -C "<repo>" worktree list --porcelain -z`, check path gone and refs resolved.

Provide to proceed: primary repo absolute path, canonical checkout path from `worktree list`, task branch name, integration ref (e.g. `main` + current commit), and confirmation of no active use + no state to preserve or discard.

