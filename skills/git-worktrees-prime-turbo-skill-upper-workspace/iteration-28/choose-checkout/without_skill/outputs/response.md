Create a new worktree, don't reuse or use current checkout.

* Don't reuse `/repo/.worktrees/login`: it has another worker's `HEAD`/index/working state. You'd clobber their uncommitted changes.
* Don't use current checkout: your unrelated uncommitted changes would mix into the fix and test results.
* New worktree gives clean isolation.

Caveat: you can't check out `feature/login` twice. `git` will refuse if it's already checked out in that worktree. Create a fix branch from it:

`git worktree add /repo/.worktrees/login-fix -b fix/login-bug feature/login`

What worktrees share vs. isolate:

* Share: repo metadata in `.git` — object DB, refs/branches/tags, remotes, config.
* Isolate per-worktree: working files, `HEAD`, index/staging, uncommitted/untracked changes.

