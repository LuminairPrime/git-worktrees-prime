## Recommendation: create a new worktree

**Not reuse** — `/repo/.worktrees/login` is owned by another worker. Reusing another worker's checkout risks clobbering their index, stepping on in-flight Git operations, and mixing two tasks' work. Coordinate with its owner if you genuinely need to share it.

**Not the current checkout** — you have unrelated uncommitted changes there. Working on `feature/login` in place would either drag those unrelated edits into your bug fix (bad commits, noisy diffs, broken review) or force you to stash/reset them, which risks discarding work. Uncommitted changes do *not* follow a new worktree automatically; they stay where they are.

**So:** create a task worktree of your own, e.g. `<primary-root>/.worktrees/login-bugfix` (or a sibling of the repo if bare), with an unused path.

**One wrinkle to check first:** `feature/login` is most likely already checked out in the existing worktree, and Git refuses to check out the same branch in two worktrees. So either:
- branch off a *different* name from the required base (`git worktree add -b <new-branch> <path> <base>`), then merge/PR into `feature/login`, or
- coordinate with the existing worktree's owner about who holds `feature/login`.

Never force past the checkout protection.

## What worktrees share vs. keep separate

**Separate per worktree:**
- Working files (the checked-out tree)
- Index / staging area
- `HEAD`
- `refs/bisect/*`, `refs/worktree/*`, `refs/rewritten/*`

**Shared across all worktrees of the repo:**
- Object database (commits, trees, blobs)
- Most refs — branches and tags (this is why a commit made in one worktree is visible in the others)
- Remotes and fetch/push configuration
- Much of the Git configuration

Practical implications:
- Sharing refs means **concurrent mutations need coordination** — two worktrees committing to or resetting the same branch will interfere.
- Sharing config means `git config --worktree` isn't isolated unless `extensions.worktreeConfig` is enabled (and only enable it if every Git installation involved supports it).
- Worktrees are **not a security boundary** — they don't isolate ports, databases, or output paths. Concurrent services need distinct ones.
- Removing a worktree leaves its branch behind; communicate the checkout path and the branch as separate things.

## Suggested sequence

1. `git worktree list --porcelain -z` to confirm the inventory (path, branch, owners).
2. If the checkout may have been moved/renamed since the task started, run `git worktree repair "<worktree>"` with its current absolute path *first* — before `cd`, `status`, or branch listing.
3. Resolve your base commit (don't assume `main`/`origin`).
4. Create your own worktree with a new branch from that base.
5. Do the fix, test, and integrate via the repo's normal merge/PR workflow — worktree creation alone doesn't authorize publishing or merging.
6. Clean up your own checkout only; leave the other worker's alone.
