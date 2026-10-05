**Recommendation: create a new worktree (option 2), don't reuse or work in the current checkout.**

## Why not the other two options

**Reusing `/repo/.worktrees/login` — No.** That worktree is owned by another worker. It may have uncommitted changes, a partially-applied patch, staged work, or a different branch state — anything you do there could collide with or corrupt their work. Only reuse a worktree if no other worker owns it.

**Working in your current checkout — No.** Your current checkout has unrelated uncommitted changes. If you fix the bug there, you risk mixing your fix with those unrelated changes (accidentally staging/committing them, stashing the wrong thing, or breaking their state). The skill calls this out explicitly: the whole point of a separate worktree is isolating this task from unrelated local changes or concurrent work.

**So: create a new task worktree.** For example:

```bash
git -C /repo worktree add -b feature/login-fix /repo/.worktrees/login-fix feature/login
```

- Use a **new branch** (`feature/login-fix`) — `feature/login` is likely already checked out at `/repo/.worktrees/login`, and a branch can't be checked out in two worktrees at once without risking state confusion.
- Keep it separate: the checkout's files, index, and `HEAD` are independent.
- Leave the existing worktree and your current checkout untouched.

## What worktrees share vs. separate

| Shared across worktrees | Per-worktree |
|---|---|
| Git object database (commits, blobs) | Working files |
| Most refs (`refs/heads/*`, tags) | Index / staging area |
| Remotes | `HEAD` |
| Most Git config | `refs/bisect/*`, `refs/worktree/*`, `refs/rewritten/*` |
| Logs/reflogs of commits | |

Key implications of sharing:

1. **No isolation boundary for Git internals** — a commit or branch update in one worktree is immediately visible in all of them. Fetches, force-pushes to local refs, etc. affect everyone.
2. **No concurrent branch checkout** — `feature/login` can only be checked out in one worktree at a time (Git enforces this via `core.worktree` protection / `git worktree list` locking).
3. **Per-worktree state only** — your uncommitted changes, staged files, HEAD, and rebase/bisect state stay local to your checkout.
4. **Shared config caveat** — don't assume `git config --worktree` isolation unless `extensions.worktreeConfig` is enabled; most settings are repository-wide.
5. **Services need separation** — dev servers, databases, ports, and output directories are not namespaced; two workers running the same app from different worktrees will still collide on port 3000 or the same database.

So: create your own worktree on a fresh branch, keep your unrelated changes undisturbed, and coordinate with the other worker through commits/branches rather than by sharing a checkout.
