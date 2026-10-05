Create a new worktree, own path. Do not reuse or work in current checkout.

* Don't reuse `/repo/.worktrees/login`: it has another worker's `HEAD`/index/working files. You'd see/conflict with their uncommitted changes.
* Don't use current checkout: you'd mix unrelated uncommitted changes into the fix.

Do: `git worktree add /repo/.worktrees/login-<you> -b fix/<bug> feature/login`

Note: you cannot check out `feature/login` twice. Git will refuse if the other worktree still has it checked out. Use a new branch from it for the fix, then merge/PR back.

What worktrees share vs isolate:

Shared: same repo — object database, refs/branches/tags, remotes, `fetch`, config in common `.git` dir.

Isolated per-worktree: working directory files, `HEAD` (checked-out branch/commit), index/staging area, uncommitted/untracked changes, build artifacts.

