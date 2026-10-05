**Short answer: No — do not prune while the share is offline. Instead, lock the worktree before it goes offline.** `git worktree lock` is the purpose-built mechanism for exactly this situation ("a worktree on a network share which is not always mounted"), and a locked worktree is never pruned by `git gc` or `git worktree prune`.

Background that drives the checklist: since Git 2.31, `git gc` — including the automatic `git gc --auto` that runs after everyday operations like commit/merge — calls `git worktree prune --expire 3.months.ago`. Pruning removes registrations whose `gitdir` file points to a missing location, but only after the grace period, and never for locked worktrees.

## Before the share goes offline (in order)

```bash
# 1. Confirm your git is new enough (lock needs >= 2.17; gc-driven prune needs >= 2.31)
git --version

# 2. Confirm the worktree is currently registered and healthy
#    (you should NOT see "prunable" next to it)
git worktree list --porcelain

# 3. Check the grace period gc would use (default: 3.months.ago)
git config --get gc.worktreePruneExpire

# 4. Sanity-check the worktree itself while it is still mounted
git -C /path/to/worktree status

# 5. Lock it — this writes .git/worktrees/<name>/locked in the MAIN repo,
#    so the protection lives on your local disk, not on the share
git worktree lock --reason "share offline 2026-10-05 to <return-date>" /path/to/worktree

# 6. Verify the lock took effect (expect a "locked" line, and NO "prunable")
git worktree list --porcelain
```

Optional belt-and-suspenders (repo-wide, affects all worktrees — the lock in step 5 is the targeted fix):

```bash
# Extend or suppress the gc grace period entirely
git config gc.worktreePruneExpire never
```

## While the share is offline

Do **not** run any of these on the main repo:

```bash
git gc            # includes gc --auto behavior; would attempt worktree pruning
git worktree prune
git maintenance run
```

Why pruning now is the wrong move:

- **Within the grace period** (default 3 months): prune would skip the worktree anyway — a pure no-op.
- **Past the grace period**: prune would destroy the registration while you cannot re-register it (the worktree directory is unmounted), leaving you to repair it later. The registration costs a tiny directory in the main repo; there is zero benefit to removing it while offline.
- If you followed step 5, neither case applies — locked worktrees are exempt regardless of age.

## When the share comes back

```bash
# 1. Confirm the registration survived
git worktree list --porcelain

# 2. If anything ever did go wrong, this re-registers the worktree
#    (commits are never lost — objects live in the shared object store)
git worktree repair /path/to/worktree

# 3. Release the lock when the share is reliably back
git worktree unlock /path/to/worktree
```

One caveat: if your git is older than 2.17, `git worktree lock` doesn't exist — upgrade git, or fall back to `git config gc.worktreePruneExpire never` (which requires >= 2.31) and avoid manual `git worktree prune` until the share returns.
