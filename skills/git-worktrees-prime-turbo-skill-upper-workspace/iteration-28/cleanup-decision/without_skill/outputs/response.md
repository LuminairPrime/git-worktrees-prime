No checkout found here to remove — verified:

* `/repo`: `No such file or directory`
* `/tmp/skill-up-3039234111`: empty, not a git repo, no `worktree list`

So no action taken. For a real repo at `/repo`, walk checks in this order — do not `rm -rf` directly:

1. List registered worktrees:
   `git -C /repo worktree list --verbose`
   Confirm `/repo/.worktrees/old-task` present, note its branch.

2. Confirm you are not inside it:
   `pwd`
   Must not be under `/repo/.worktrees/old-task` when removing it.

3. Check clean status inside worktree:
   `git -C /repo/.worktrees/old-task status --porcelain`
   `git -C /repo/.worktrees/old-task rev-parse --abbrev-ref HEAD`
   Must be empty output; stash/commit anything to keep.

4. Check merge — squash matters:
   `git -C /repo branch --merged main` will *not* list a squash-merged branch, and `git -C /repo merge-base --is-ancestor <branch> main` will fail. This is expected. Verify merge externally e.g. `git -C /repo log --oneline main -5` contains squash commit / PR merged, not via `is-ancestor`.

5. Remove checkout only after 1-4 pass:
   `git -C /repo worktree remove /repo/.worktrees/old-task`
   Use `--force` only if 3 showed intentional discard. Re-verify with `worktree list`.

6. Delete branch, after removal:
   `git -C /repo branch -d <branch>`
   Expected to fail for squash. Only after 4 is confirmed, retry:
   `git -C /repo branch -D <branch>`

7. Prune stale metadata:
   `git -C /repo worktree prune -v`
   `git -C /repo worktree list`

