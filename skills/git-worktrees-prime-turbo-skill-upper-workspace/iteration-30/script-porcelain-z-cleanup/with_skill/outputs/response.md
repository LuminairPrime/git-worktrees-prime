Per `references/raw-git-commands.md#cleanup`: use `git worktree remove`, parse `list --porcelain -z`, prune with same options as dry-run.

Checks + script in order:

1. Leave task checkout, verify repo and inventory:
```sh
cd /repo
pwd # must not be inside /repo/.worktrees/<task> being removed
git -C "/repo" worktree list
git -C "/repo" worktree list --porcelain -z
```

2. Preservation check per candidate — clean does not cover ignored/detached:
```sh
git -C "<candidate-worktree>" status --short --branch --untracked-files=all
git -C "<candidate-worktree>" status --short --ignored
git -C "<candidate-worktree>" rev-parse HEAD
```

3. Remove only registered paths under base that still exist:
```bash
set -euo pipefail
REPO="/repo"
BASE="/repo/.worktrees"
git -C "$REPO" worktree list --porcelain -z |
while IFS= read -r -d '' entry; do
  case "$entry" in
    worktree\ *)
      wt="${entry#worktree }"
      case "$wt" in
        "$BASE"/*)
          if [ -d "$wt" ]; then
            git -C "$REPO" worktree remove "$wt"
          else
            printf 'skip missing: %s\n' "$wt"
          fi
          ;;
      esac
      ;;
  esac
done
```

4. Verify removals, then prune only reviewed entries:
```sh
git -C "/repo" worktree list --porcelain -z
git -C "/repo" worktree prune --dry-run --verbose
# review every line: must all be intentionally removed; missing dir may be offline — do not prune
git -C "/repo" worktree prune --verbose
git -C "/repo" worktree list
```
Prune removes registrations only, not branches/directories.

