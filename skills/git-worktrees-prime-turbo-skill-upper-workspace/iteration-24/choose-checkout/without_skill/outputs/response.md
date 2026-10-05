Create a new worktree, do not reuse or use current checkout.

* Do not reuse `/repo/.worktrees/login`: owned by another worker — shared `HEAD`/index/working files would clobber, one branch cannot be checked out in 2 worktrees at once.
* Do not use current checkout: has unrelated uncommitted changes — you would have to `stash`/`switch` and risk mixing them into the fix.
* Do: `git worktree add /repo/.worktrees/login-fix -b fix/login-bug feature/login` — isolated dir from `feature/login` tip.

Worktrees share: same repo — `objects`, `refs/branches/tags`, `config`, remotes. Private per-worktree: working directory, `HEAD`, `index`/staged + uncommitted changes.

