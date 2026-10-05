Here's the script with its checks, in order:

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO="/repo"
WORKTREE_ROOT="${REPO}/.worktrees"

# ── Checks ──────────────────────────────────────────────────────────

# 1. git must be available
command -v git >/dev/null 2>&1 || { echo "error: git not found" >&2; exit 1; }

# 2. /repo must exist and be a git repository
[[ -d "$REPO" ]] || { echo "error: $REPO does not exist" >&2; exit 1; }
[[ -d "$REPO/.git" ]] || { echo "error: $REPO is not a git repository" >&2; exit 1; }

# 3. .worktrees directory must exist
[[ -d "$WORKTREE_ROOT" ]] || { echo "error: $WORKTREE_ROOT does not exist" >&2; exit 1; }

# ── Remove linked task checkouts whose directories still exist ───────

# 4. Find linked task checkouts under /repo/.worktrees
#    and remove each one whose directory still exists on disk.
#    --porcelain output is parsed with sed; the while-read loop
#    preserves paths containing spaces.
git -C "$REPO" worktree list --porcelain \
  | sed -n 's/^worktree //p' \
  | while IFS= read -r wt; do
      case "$wt" in
          "$WORKTREE_ROOT"/*)
              if [[ -d "$wt" ]]; then
                  echo "Removing worktree: $wt"
                  git -C "$REPO" worktree remove --force "$wt"
              else
                  echo "Skipping (directory already gone): $wt"
              fi
              ;;
      esac
  done

# 5. Prune stale registrations (directories that no longer exist).
git -C "$REPO" worktree prune
```

**How it handles spaces:** `git worktree list --porcelain` emits one `worktree <path>` line per checkout. `sed` strips the prefix, and `while IFS= read -r wt` reads the whole line without word-splitting, so paths with spaces stay intact. Every use of `"$wt"` is quoted.

**What each step does:**

| Step | Purpose |
|------|---------|
| 1–3 | Fail fast if git, the repo, or `.worktrees` is missing |
| 4 | Lists all worktrees, filters to those under `.worktrees`, and removes only those whose directory still exists on disk |
| 5 | Cleans up `.git/worktrees/` metadata for any registration whose directory is already gone |
