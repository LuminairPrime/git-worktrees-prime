**Create a new, separate worktree.** Don't reuse the existing one and don't work in your current checkout.

**Why:**

1. **Reusing `/repo/.worktrees/login` is off the table** — another worker owns it. Worktrees are the unit of ownership: two agents editing the same path (and likely the same `feature/login` branch) would clobber each other's index, files, and in-progress operations. Also, a branch can only be checked out in one worktree at a time unless you use detached HEAD, so you'd have to steal or override their branch — don't.

2. **Working in your current checkout is also wrong** — it has unrelated uncommitted changes. Mixing your bug fix with those changes risks contaminating commits, and any stash/reset/clean to "make room" could destroy someone's work. Worktrees exist precisely for this: concurrent work on different branches without disturbing each other.

3. **So: create a new task worktree**, e.g. `/repo/.worktrees/login-bugfix` (or a distinct name), on its own branch (e.g. `fix/login-bug`) created from the correct base — inspect the repo's normal integration target rather than assuming `main`, fetch the relevant remote ref if needed, and never `git pull` into the other worker's checkout. Before creating, verify `/.worktrees/` is git-ignored (`git check-ignore -q ".worktrees/"` from the enclosing checkout) so the new directory doesn't pollute status.

**What worktrees share (and don't):**

- **Separate per worktree:** working files, the index/staging area, `HEAD`, and `refs/bisect/*`, `refs/worktree/*`, `refs/rewritten/*`.
- **Shared across all worktrees:** the object database (commits, trees, blobs), most refs including remote-tracking refs, remotes, and most Git configuration.

Practical consequences: committing in your new worktree immediately makes those objects visible to the other worker's repo, but it won't move their `HEAD` or touch their files. Branch creation by one worktree affects branches another can see. And there's **no security or resource isolation** — concurrent services (dev servers, tests) need distinct ports, databases, and output dirs.

**Before creating**, confirm the inventory with `git worktree list --porcelain` and read `references/raw-git-commands.md` (creation section) before running raw `git worktree add` — use `-b` for a new branch, never `-B`, which would reset the branch without authorization.
