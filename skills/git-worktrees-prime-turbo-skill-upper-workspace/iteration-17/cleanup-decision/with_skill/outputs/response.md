In this environment `/repo/.worktrees/old-task` does not exist — `/repo` not found, current dir is not a git repo — so I cannot authorize `remove` / `branch -d` / `prune` yet. Walkthrough in order, per cleanup decision tree:

1. **Still in use?** Confirm no agent, editor, terminal, service, or test is using `/repo/.worktrees/old-task`. Leave dir before removal. Do not clean another worker's checkout.
2. **Still needed for review?** If review can continue from preserved commits, checkout may go before merge; otherwise retain.
3. **State would disappear?** From the checkout run:
   - `git -C "<worktree>" status --short --branch --untracked-files=all`
   - `git -C "<worktree>" status --short --ignored`
   - `git -C "<worktree>" rev-parse HEAD`
   Check detached commits, unfinished ops, submodules/nested repos separately. Preserve or get authorization to discard. Clean status does not prove ignored files/detached commits are safe.
4. **Safe to remove checkout? BLOCKED:** Need canonical path + ownership from:
   - `git -C "<repo>" worktree list --porcelain -z`
   Removing a worktree leaves its branch — name path vs branch separately. Remove only exact task checkout via manager or `git -C "<repo>" worktree remove "<worktree>"`, from a surviving checkout. Never `rm -rf` the directory, never prune a live checkout. You did not provide the task branch name.
5. **Safe to delete branch? BLOCKED — squash case:** Need task-branch name and verified current integration ref. Then:
   - `git -C "<repo>" merge-base --is-ancestor "<task-tip>" "<integration-ref>"`
   With squash this will likely exit non-zero — expected, needs review. `branch -d` success is not integration evidence, it may check upstream not the target. Verify replacement commits and resulting changes (e.g. diff of task tip vs target contains no missing work). Only if verified integrated/preserved/authorized for abandonment, run `git -C "<repo>" branch -d "<task-branch>"`. If it refuses, retain; only consider `-D` after obsolete history is verified safe + authorized.
6. **Prune?** Only for intentionally removed worktrees:
   - `git -C "<repo>" worktree prune --dry-run --verbose`
   Review every entry — a missing dir may be offline volume, do not prune/unlock it. Then `git -C "<repo>" worktree prune --verbose` with same expiry options.
7. **Verify:** `git -C "<repo>" worktree list --porcelain -z`, check path gone, chosen refs gone. Report retained items + why.

To proceed, provide: primary `<repo>` path, task branch name + `HEAD` from step 3, integration target ref + how squash was verified.

