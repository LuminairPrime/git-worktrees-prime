Before the share is unmounted, verify the registration and lock the worktree. Do **not** prune it while it is unavailable.

Set:

- `<repo>` — main checkout or bare repository path
- `<worktree>` — the task checkout's current absolute path
- `<reason>` — e.g. `"network share offline for active task"`

### While the share is mounted

```sh
git -C "<repo>" worktree list --porcelain -z
```

Confirm the task appears at `<worktree>` and record its branch or detached HEAD. If its path has changed since registration, repair it first:

```sh
git -C "<repo>" worktree repair "<worktree>"
git -C "<repo>" worktree list --porcelain -z
```

Verify the live checkout:

```sh
git -C "<worktree>" rev-parse --show-toplevel
git -C "<worktree>" status --short --branch --untracked-files=all
git -C "<worktree>" rev-parse HEAD
```

Check that it is not currently considered prunable:

```sh
git -C "<repo>" worktree prune --dry-run --verbose
```

The task worktree must **not** appear in the dry-run output.

Optionally inspect the configured GC grace period:

```sh
git -C "<repo>" config --get gc.worktreePruneExpire || true
```

Lock the registration before unmounting:

```sh
git -C "<repo>" worktree lock --reason "<reason>" "<worktree>"
git -C "<repo>" worktree list --porcelain -z
git -C "<repo>" worktree list --verbose
```

Confirm the target now has a line such as:

```text
locked <reason>
```

and is not marked `prunable`. You can also repeat:

```sh
git -C "<repo>" worktree prune --dry-run --verbose
```

It must still not list the task worktree.

### While the share is offline

Do **not** run these against that worktree:

```sh
git -C "<repo>" worktree prune
git -C "<repo>" worktree unlock "<worktree>"
git -C "<repo>" worktree remove "<worktree>"
```

Its absence while unmounted is not evidence that the registration is stale. With the lock in place, normal GC should not prune its worktree administrative files.

### When the share returns

```sh
git -C "<repo>" worktree list --porcelain -z
git -C "<worktree>" rev-parse --show-toplevel
git -C "<worktree>" status --short --branch --untracked-files=all
git -C "<worktree>" rev-parse HEAD
```

If its path changed during the outage, repair first:

```sh
git -C "<repo>" worktree repair "<worktree>"
git -C "<repo>" worktree list --porcelain -z
```

Only unlock after confirming the stored reason and when the task no longer needs that offline protection:

```sh
git -C "<repo>" worktree list --verbose
git -C "<repo>" worktree unlock "<worktree>"
git -C "<repo>" worktree list --porcelain -z
```

Prune only after reviewing a dry run where every entry is intentionally removed, never because the active task's share is temporarily inaccessible:

```sh
git -C "<repo>" worktree prune --dry-run --verbose
git -C "<repo>" worktree prune --verbose
```
