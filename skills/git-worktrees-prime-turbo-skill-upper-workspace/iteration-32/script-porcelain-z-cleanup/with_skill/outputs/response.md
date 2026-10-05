## Checks and script, in order

**1. Confirm the repository and inventory (before touching anything):**

```bash
git -C /repo rev-parse --show-toplevel
git -C /repo worktree list --porcelain -z
```

**2. Per linked checkout under `/repo/.worktrees`, run the state checks** (clean status does not prove preservation of ignored files or detached commits, so capture both):

```bash
git -C "<checkout>" status --short --branch --untracked-files=all
git -C "<checkout>" status --short --ignored
git -C "<checkout>" rev-parse HEAD
```

Only proceed for checkouts the cleanup decision tree permits you to remove (not owned by another worker, no needed state in the directory).

**3. The script** (safe for task names with spaces — it parses `git worktree list --porcelain -z` NUL-delimited fields, never splits on whitespace):

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO=/repo
BASE="$REPO/.worktrees"

# Collect candidate linked checkouts first; removal changes the list.
paths=()
while IFS= read -r -d '' field || [[ -n "$field" ]]; do
  case "$field" in
    "worktree "*)
      p="${field#worktree }"
      if [[ "$p" == "$BASE/"* && "$p" != "$REPO" ]]; then
        paths+=("$p")
      fi
      ;;
  esac
done < <(git -C "$REPO" worktree list --porcelain -z)

for p in "${paths[@]}"; do
  # Remove only if the directory still exists on disk;
  # missing directories are stale registrations handled by prune.
  if [[ -d "$p" ]]; then
    git -C "$REPO" worktree remove -- "$p"
  fi
done

# Prune stale registrations (empty records = removed/missing checkouts).
git -C "$REPO" worktree prune --verbose
```

Notes on the script's choices:

- Plain `git worktree remove` is used, not `--force`: a dirty or locked checkout fails loudly so you can inspect rather than silently discard state. Add `--force` only after the step-2 checks and authorization.
- `--` after `worktree remove` guards against paths beginning with `-`.
- Collecting paths before removing avoids mutating the inventory mid-iteration.

**4. Review the prune dry run before pruning** (every entry must be an intentionally removed worktree — not a missing directory on an offline volume):

```bash
git -C /repo worktree prune --dry-run --verbose
```

Do **not** prune (or unlock) a merely unavailable/offline checkout. If the dry run is clean, run the prune shown in the script.

**5. Verify the result:**

```bash
git -C /repo worktree list --porcelain -z
```

Confirm each removed path is gone from the list and no registration remains for it. Branch deletion and archive/snapshot cleanup are separate decisions — this script intentionally leaves branches and history intact.
