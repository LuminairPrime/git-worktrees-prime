Do **not** prune while the share is unavailable — a missing directory during an outage can look like a stale registration, and pruning would destroy the link you need when the share returns. Protect it instead by locking it before the offline window. Exact steps, in order:

**1. Confirm the current registration and state**

```sh
git -C "<repo>" worktree list --porcelain -z
git -C "<worktree>" status --short --branch
git -C "<worktree>" rev-parse HEAD
git -C "<worktree>" rev-parse --show-toplevel
```

Check the output agrees: the registered path, branch, HEAD commit, and `--show-toplevel` path all match the live checkout.

**2. Repair if anything drifted** (e.g., the mount path changed at some point). Only if the path no longer matches:

```sh
git -C "<repo>" worktree repair "<worktree>"   # use the checkout's current absolute path
git -C "<repo>" worktree list --porcelain -z   # verify the registration now points at the right path
```

**3. Lock the worktree before the share goes offline**

```sh
git -C "<repo>" worktree lock --reason "offline share until <date>" "<worktree>"
```

Verify the lock took effect:

```sh
git -C "<repo>" worktree list --porcelain -z   # expect a "locked" line with your reason
git -C "<repo>" config --get-all gc.worktreePruneExpire   # know your gc expiry setting, if set
```

**4. While offline: do nothing destructive.** Specifically, while the share is unmounted:

- Do **not** run `git worktree prune` (even with `--dry-run` as a cleanup step — its real run would hit this worktree).
- Do **not** run `git worktree unlock` — an absent directory is not permission, and it's not stale.
- Avoid `git gc`/`git gc --auto` against the shared repository if you can; that's where `gc.worktreePruneExpire` would normally expire missing registrations. The lock from step 3 is what shields the registration, so keep the lock reason intact and don't delete the `locked` marker file.

**5. When the share is back: unlock only after verifying the checkout is truly there**

```sh
git -C "<worktree>" rev-parse --show-toplevel   # must succeed and match the registered path
git -C "<repo>" worktree list --porcelain -z     # confirm registered path and branch
git -C "<repo>" worktree unlock "<worktree>"
git -C "<repo>" worktree list --porcelain -z     # locked line should be gone
git -C "<worktree>" status --short --branch
```

Only if step 5's checks fail should you investigate with `git worktree repair "<current-path>"` — and only prune (`git worktree prune --dry-run --verbose`, review every entry, then `git worktree prune --verbose`) for worktrees you intentionally removed. A merely unavailable checkout on an offline share is never a prune candidate.

Substitute `<repo>` (main checkout or bare repo), `<worktree>` (the task checkout's absolute path on the share), and a concrete date in the lock reason.
