## 1. Establish the inventory

```bash
git -C /repo worktree list --porcelain -z
```

## 2. Per-candidate safety checks (run for each checkout under `/repo/.worktrees/`)

```bash
# Clean status does not establish preservation of ignored files or detached commits.
git -C "<worktree>" status --short --branch --untracked-files=all
git -C "<worktree>" status --short --ignored
git -C "<worktree>" rev-parse HEAD

# Exit 0 proves this tip is an ancestor of this target. Other outcomes need review.
git -C /repo merge-base --is-ancestor "<task-tip>" "<integration-ref>"
```

## 3. Removal + prune script

```bash
git -C /repo worktree list --porcelain -z | while IFS= read -r -d '' field; do
  if [[ $field == worktree\ * ]]; then
    wt=${field#worktree }
  elif [[ -z $field || $field == HEAD\ * || $field == branch\ * || $field == detached ]]; then
    if [[ -z $field && -n $wt ]]; then
      case $wt in
        /repo/.worktrees/*)
          # Remove only if the cleanup decision tree permits checkout removal.
          if [[ -d $wt ]]; then
            git -C /repo worktree remove "$wt"
          fi
          ;;
      esac
      wt=
    fi
  fi
done
```

## 4. Verify the result

```bash
git -C /repo worktree list --porcelain -z
```

## 5. Prune stale registrations (review every dry-run entry first; prune only intentionally removed worktrees)

```bash
git -C /repo worktree prune --dry-run --verbose
git -C /repo worktree prune --verbose
```

Notes:
- `--porcelain -z` + `read -d ''` is required because task names may contain spaces.
- `[ -d "$wt" ]` removes only registrations whose directory still exists on disk; missing directories are left for the prune step (a missing directory may be an offline volume — do not prune or unlock one just because it is unavailable).
- The primary checkout, the current working directory, and sibling tasks outside `/repo/.worktrees/` are excluded by the path filter.
- `worktree remove` uses Git's own removal (never `rm -rf`); prune removes stale metadata only, not branches or live checkout directories.
