Do this **while the share is still mounted**, in this order:

1. Confirm the registration and the worktree's current path/branch:
   ```sh
   git -C "<repo>" worktree list --porcelain -z
   git -C "<worktree>" status --short --branch
   git -C "<worktree>" rev-parse HEAD
   ```

2. Push/finalize any task work you want preserved outside that share (commit, push, or otherwise record the tip).

3. Check what expiry `git gc` would use for missing worktree registrations:
   ```sh
   git -C "<repo>" config --get-all gc.worktreePruneExpire
   ```
   (If unset, Git uses its default expiry window; a mounted worktree should never appear, but a missing one can be pruned by `git gc`/`worktree prune`.)

4. Prove it is *not* currently stale, while everything is mounted:
   ```sh
   git -C "<repo>" worktree prune --dry-run --verbose
   ```
   The task worktree must **not** be listed. If it is, repair/re-register it first (`git -C "<repo>" worktree repair "<worktree>"`) and re-list — do not lock/prune around a registration that already looks broken.

5. Lock the worktree before the share goes offline, with an explicit reason:
   ```sh
   git -C "<repo>" worktree lock --reason "share offline from <date>; task active, mounted again later" "<worktree>"
   ```

6. Verify the lock is recorded:
   ```sh
   git -C "<repo>" worktree list --porcelain -z
   git -C "<repo>" worktree list
   ```
   Look for the `locked ...` attribute on that worktree. Keep the reason text somewhere you'll read before unlocking.

While the share is offline: **do not prune** its registration and **do not unlock** it. A missing directory may just be an unavailable volume; `git -C "<repo>" worktree prune` (or `git gc`, which runs worktree pruning via `gc.worktreePruneExpire`) would treat it as stale without the lock. The lock is what keeps Git from dropping that registration while the storage is detached.

When the share is back: mount it, then verify with `git -C "<repo>" worktree list --porcelain -z`; if the path changed, repair with `git -C "<repo>" worktree repair "<current-absolute-path>"` and re-list. Only unlock afterward if you intend the intermittent-mount protection to end: `git -C "<repo>" worktree unlock "<worktree>"` (read the stored reason first). Only prune later if the checkout is intentionally removed/destroyed, and even then review `git worktree prune --dry-run --verbose` first — never prune just because it was unavailable.
