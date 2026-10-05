Create a new worktree, do neither of the others:

1. Don't reuse `/repo/.worktrees/login`: it's owned/active by another worker. You'd see/clobber their uncommitted state and step on their `HEAD`.
2. Don't use current checkout: it has unrelated uncommitted changes you'd mix into the fix.

Run `git worktree list` to confirm, then add your own:
`git worktree add /repo/.worktrees/login-fix -b fix/login-bug feature/login`

Note: you can't checkout `feature/login` twice - Git forbids the same branch in 2 worktrees. Use a new fix branch off it.

What worktrees share: same repo - `.git/objects`, `refs/branches/tags`, remotes, config, fetch state. A branch/fetch in one is visible in all.

What they don't share: working directory, `HEAD`, index/staging, uncommitted changes. That's why isolation is safe.

