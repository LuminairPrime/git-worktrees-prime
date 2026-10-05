Create a new worktree, don't reuse or use current checkout.

* Don't reuse `/repo/.worktrees/login`: owned by another worker — you'd clobber their uncommitted work, and git forbids the same branch `feature/login` checked out in 2 worktrees.
* Don't use current checkout: unrelated uncommitted changes would mix into the fix.

Create separate worktree with a new branch off `feature/login`:

`git worktree add /repo/.worktrees/login-fix -b fix/login-bug feature/login`

Worktrees share: same repo — `.git` dir, object database, refs/branches, remotes, config. Isolated per-worktree: working directory, `HEAD`/checked-out branch, index/staging area, uncommitted changes.
