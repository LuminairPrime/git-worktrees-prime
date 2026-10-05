In this session `/repo` does not exist, so I cannot execute removal here — verified with `git worktree list` / `ls /repo`:

* `/tmp/skill-up-2143639885` is empty, not a git repo
* No `/repo/.worktrees/old-task`

Run this in order from `/repo`:

1. **Confirm checkout exists:**
   `git worktree list --verbose` — should show `/repo/.worktrees/old-task` + branch name.
2. **Not inside it:**
   `pwd; git rev-parse --show-toplevel` — must be `/repo`, not `old-task`. `cd /repo` first.
3. **Clean + pushed:**
   `git -C /repo/.worktrees/old-task status --porcelain` — must be empty. `git -C /repo/.worktrees/old-task log --branches --not --remotes --oneline` to check unpushed.
4. **Verify squash-merge:**
   Squash breaks `git branch -d` ancestry detection, so `git branch --merged main` will likely *not* list it. Verify via PR merged status or `git log --oneline main | head` contains the squash commit, and `git cherry main <branch>` is empty.
5. **Remove checkout:**
   `git worktree remove /repo/.worktrees/old-task` — add `--force` only if step 3 showed junk you intend to discard.
6. **Delete branch:**
   `git branch -d <branch>` will fail with `not fully merged` for squash — expected. After step 4 verification, use `git branch -D <branch>`.
7. **Prune + verify:**
   `git worktree prune -v; git worktree list; git branch -a | grep old-task` — worktree gone, branch gone, no `prunable` entries.

