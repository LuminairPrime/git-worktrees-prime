Pre / post checks with cleanup in order:

```bash
git rev-parse --show-toplevel
git worktree list
ls -la "/repo/.worktrees"
```

```bash
set -euo pipefail
git worktree list --porcelain | while IFS= read -r line; do
  case "$line" in
    "worktree "*)
      wt="${line#worktree }"
      case "$wt" in
        /repo/.worktrees/*)
          if [ -d "$wt" ]; then
            git worktree remove --force "$wt"
          fi
          ;;
      esac
      ;;
  esac
done
git worktree prune
```

```bash
git worktree list
ls -la "/repo/.worktrees"
```
