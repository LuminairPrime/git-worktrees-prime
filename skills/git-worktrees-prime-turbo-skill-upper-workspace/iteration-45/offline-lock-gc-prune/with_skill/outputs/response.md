## Before the storage goes offline

Run these in order, from a checkout that is *not* on the going-offline share (the main/bare repo, `<repo>`).

**1. Inventory the registration (read-only).**

```sh
git -C "<repo>" worktree list --porcelain -z
```

Confirm the task worktree's entry, its branch/`HEAD`, and that it is not already `locked`. Record its `HEAD` commit now:

```sh
git -C "<worktree>" rev-parse HEAD
```

**2. Repair first if the mount path may have shifted** (reorganization, rename, mount-point change). Repair reconnects the registration; it does not touch the index, branch, or state.

```sh
git -C "<repo>" worktree repair "<worktree>"
git -C "<repo>" worktree list --porcelain -z
```

Do not start with `status`, `checkout`, or branch listing — repair comes first when the path may have moved.

**3. While the share is still mounted, make sure nothing valuable lives only there.**

```sh
git -C "<worktree>" status --short --branch --untracked-files=all
git -C "<worktree>" status --short --ignored
```

Commit or otherwise preserve tracked changes, untracked/ignored files, and any detached commits; finish or safely abort any in-progress Git operation. Commit/push the task branch so its history survives independent of the checkout.

**4. Lock the worktree — this is the actual protection against `git gc`.**

```sh
git -C "<repo>" worktree lock --reason "share <name> offline <dates>; task still active" "<worktree>"
```

A locked registration is exempt from automatic pruning (`gc.worktreePruneExpire`, default 3 months), so `git gc` will not drop it while the directory is unmounted. The reason flag precedes the path.

**5. Verify the lock took effect.**

```sh
git -C "<repo>" worktree list --porcelain -z
```

Confirm the entry now carries `locked` plus your reason. Re-check the branch and `HEAD` from step 1 are unchanged.

## Should you prune the registration while it is unavailable?

**No. Do not run `git worktree prune` at all** — not with `--force`, not with a custom expiry, not "just to tidy up."

- A missing directory is consistent with an offline volume; pruning there destroys a live registration for a checkout that still exists and is still needed.
- Never prune or unlock a merely unavailable checkout, and never prune with expiry options other than a reviewed dry run.

If you want visibility only (optional, still no mutation, and only once the path is known missing):

```sh
git -C "<repo>" worktree prune --dry-run --verbose
```

Treat every line as review material, not a to-do. While the share is offline, exit without running the real `prune`.

## When the storage comes back

```sh
git -C "<repo>" worktree list --porcelain -z     # confirm still registered + locked, read the reason
git -C "<repo>" worktree repair "<worktree>"     # only if the mount path changed
git -C "<repo>" worktree list --porcelain -z     # re-verify registration
git -C "<worktree>" status --short --branch       # confirm checkout is intact
git -C "<repo>" worktree unlock "<worktree>"      # only after reading the reason and confirming it's no longer needed
```

Keep the lock until the checkout is confirmed reachable and healthy; unlock only then.
