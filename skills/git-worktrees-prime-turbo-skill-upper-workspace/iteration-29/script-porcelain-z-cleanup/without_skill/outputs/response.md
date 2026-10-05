```bash
set -euo pipefail

# 1. Pre-checks
test -d /repo/.worktrees
git -C /repo rev-parse --is-inside-work-tree
git -C /repo worktree list
find /repo/.worktrees -mindepth 1 -maxdepth 1 -print

# 2. Remove each existing checkout; space-safe
find /repo/.worktrees -mindepth 1 -maxdepth 1 -type d -print0 | while IFS= read -r -d '' wt; do
  if [ -d "$wt" ]; then
    git -C /repo worktree remove --force "$wt"
  fi
done

# 3. Prune stale registrations
git -C /repo worktree prune -v

# 4. Post-checks
git -C /repo worktree list
find /repo/.worktrees -mindepth 1 -maxdepth 1 -print
```
