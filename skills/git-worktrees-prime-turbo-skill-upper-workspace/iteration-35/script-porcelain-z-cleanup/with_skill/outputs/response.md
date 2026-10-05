## Checks and script, in order

**1. Inventory the linked checkouts before touching anything** (NUL-delimited so spaces in task names survive):

```sh
git -C /repo worktree list --porcelain -z
git -C /repo status --short --branch   # only if /repo is a checkout, not bare
```

**2. Per-checkout safety check** before removal (repeat for each path under `/repo/.worktrees/`; clean `status` does not prove ignored files or detached commits are preserved):

```sh
git -C "<worktree>" status --short --branch --untracked-files=all
git -C "<worktree>" status --short --ignored
git -C "<worktree>" rev-parse HEAD
```

Skip any checkout that still shows needed state, is still in use, or is a possibly-offline volume — do not let the script's removal stand in for this review.

**3. The removal script** (parses `--porcelain -z`, handles spaces in names, removes only paths under `/repo/.worktrees` whose directory still exists — missing ones are left for prune or repair, never force-removed):

```bash
git -C /repo worktree list --porcelain -z | while IFS= read -r -d '' tok; do
  case "$tok" in
    "worktree "*)
      path="${tok#worktree }"
      case "$path" in
        /repo/.worktrees/*) ;;
        *) continue ;;
      esac
      [ -d "$path" ] || continue
      git -C /repo worktree remove "$path" || exit 1
      ;;
  esac
done
```

No `--force`: a dirty or locked checkout makes `worktree remove` fail and must be resolved (commit, discard by authorization, or repair), not overridden.

**4. Verify the removal:**

```sh
git -C /repo worktree list --porcelain -z
```

**5. Review every dry-run prune entry** — prune only if each is a worktree you intentionally removed. A missing directory may be an offline volume; do not prune those.

```sh
git -C /repo worktree prune --dry-run --verbose
```

**6. Prune stale registrations** (same options as the reviewed dry run; no `--expire` override):

```sh
git -C /repo worktree prune --verbose
```

**7. Final verification and report:**

```sh
git -C /repo worktree list --porcelain -z
git -C /repo status --short --branch
```

Report anything retained, and note that pruning removes only metadata — branches remain unless separately deleted with `git -C /repo branch -d "<task-branch>"` after verifying the tip is integrated.
