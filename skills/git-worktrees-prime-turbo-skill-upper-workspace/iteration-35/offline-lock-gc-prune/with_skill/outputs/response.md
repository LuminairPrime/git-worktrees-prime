Short answer: **lock it before the share goes offline, and do not prune — or unlock — while it's unavailable.** A missing directory is expected for an offline volume; Git can't distinguish "temporarily unmounted" from "deleted," and `gc` will prune stale registrations automatically, so the lock is what protects the registration.

Run everything from the main checkout or bare repository.

## 1. Before the storage goes offline

Inventory the registration and record its state (so you can compare later):

```sh
git -C "<repo>" worktree list --porcelain -z
# Record the exact absolute path, branch, and lock state.
git -C "<worktree>" rev-parse HEAD
git -C "<worktree>" status --short --branch
```

Confirm you have the correct path and branch (don't lock the wrong checkout), then lock it with a reason that explains the outage window:

```sh
git -C "<repo>" worktree lock --reason "share offline <start–end date>; task active" "<worktree>"
```

Verify the lock actually took effect:

```sh
git -C "<repo>" worktree list --porcelain -z
# Expect a "locked" entry (and the reason) for <worktree>.
```

Optionally confirm the auto-prune setting you're guarding against:

```sh
git -C "<repo>" config --get gc.worktreePruneExpire
```

The lock is the real protection; you don't need to change `gc.worktreePruneExpire`.

## 2. While the share is unavailable

Do **not** run any of these:

- `git worktree prune` (nor `prune --dry-run`, if a stale entry would tempt you)
- `git worktree unlock "<worktree>"`
- `git worktree remove "<worktree>"`
- `git worktree repair` against a path that isn't mounted

The registration is not obsolete, just unreachable; leave it locked. If `git worktree list` complains about the missing path, that's expected and harmless.

## 3. When the storage comes back online

If the path is unchanged, the lock alone preserved it — verify and then unlock when the task no longer needs protection:

```sh
git -C "<repo>" worktree list --porcelain -z
git -C "<worktree>" rev-parse HEAD          # compare to the recorded commit
git -C "<repo>" worktree unlock "<worktree>"
```

If the path changed (remount at a new location, rename, reorg), **repair first** — `git worktree repair` reconnects the live checkout and preserves its branch, index, and state:

```sh
git -C "<repo>" worktree repair "<worktree>"   # current absolute path
git -C "<repo>" worktree list --porcelain -z  # verify new registration
```

Then unlock once you've read and cleared the original reason.

Cleanup of the registration only belongs *after* the task is done and the checkout is intentionally removed — at that point review `git worktree prune --dry-run --verbose` and require every entry to be an intentionally removed worktree before pruning.
