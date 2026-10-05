**Answer up front: lock the worktree before the share goes offline, and do *not* prune its registration while it's unavailable.** A locked worktree is never selected by `git worktree prune` (which `git gc` invokes), so the registration survives the outage. An unmounted checkout that merely looks missing is exactly the false-positive that pruning would destroy.

Here is the exact sequence, in order. `<repo>` = the main checkout or bare repository (the admin data lives there); `<worktree>` = the task checkout's current absolute path on the share.

## Before the storage goes offline

**1. Inventory — read, don't act.**

```sh
git -C "<repo>" worktree list --porcelain -z
```

Confirm `<worktree>` appears, note its `HEAD`, `branch`, and any `locked` / `prunable` lines. This is your baseline; keep it.

**2. Confirm the registration is live *while the share is still mounted*.**

```sh
git -C "<worktree>" rev-parse --show-toplevel
git -C "<worktree>" rev-parse HEAD
git -C "<worktree>" status --short --branch --untracked-files=all
```

**3. If the path or mount point ever shifted, repair first — before any other decision.**

```sh
git -C "<repo>" worktree repair "<worktree>"
git -C "<repo>" worktree list --porcelain -z
```

Repair reconnects the registration and preserves the branch, index, and state. Do not substitute prune, remove, or recreate for a repair.

**4. Preserve anything that exists only on that share.**

```sh
git -C "<worktree>" status --short --ignored
git -C "<worktree>" log --oneline "<integration-ref>..HEAD"
```

Push unpushed commits or copy off untracked/ignored files you need. Per-worktree refs (`refs/bisect/*`, `refs/worktree/*`, `refs/rewritten/*`) live under the main repo's admin directory, not the share — but detached commits reachable only from that checkout's `HEAD` do not.

**5. Lock it — the reason flag precedes the path.**

```sh
git -C "<repo>" worktree lock --reason "<share-offline-dates>; task <id> still active" "<worktree>"
git -C "<repo>" worktree list --porcelain -z
```

Verify a `locked` line carrying your reason now appears. Optionally record the prune window: `git config --get gc.worktreePruneExpire` (default is generous, but the lock is the actual guarantee).

## While the share is unavailable

**Do not run any of these:**

- `git worktree prune` — not even "just the stale ones." Missing path ≠ removed worktree; it may be an offline volume.
- `git worktree unlock` — an absent or unreadable checkout is not a reason to unlock.
- `git worktree remove`, `branch -d`, or any hand-editing of `.git/worktrees/<name>/` metadata or directory deletion through filesystem tools.

A `prune --dry-run` is safe to *read* for orientation, but take no action on its output while the checkout is unavailable, and do not later prune with expiry options different from the reviewed dry run.

## When the storage returns

```sh
git -C "<repo>" worktree list --porcelain -z        # read the stored lock reason first
git -C "<repo>" worktree repair "<worktree>"        # only if the path/mount moved
git -C "<worktree>" rev-parse --show-toplevel
git -C "<worktree>" status --short --branch
git -C "<repo>" worktree unlock "<worktree>"
git -C "<repo>" worktree list --porcelain -z        # confirm clean registration, lock gone
```

**One caveat:** this protects a *linked* checkout whose repository admin data stays reachable. If the main repository itself is on the going-offline share, there is nothing for another machine's `gc` to prune — but there is also nothing from which to run these commands while it's down, so do step 4 (preservation) first and take a full backup of `.git/worktrees/`.
