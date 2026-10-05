In order, with `/repo` as `<repo>`:

**1. Verify inventory — do not delete by directory listing alone:**
```sh
git -C "/repo" worktree list --porcelain -z
git -C "/repo" rev-parse --show-toplevel
pwd # must not be inside a target under /repo/.worktrees
```
Scripts must parse `git worktree list --porcelain -z` — `references/raw-git-commands.md:42-63`.

**2. Per-candidate preservation checks — retain on any failure:**
```sh
git -C "<worktree>" status --short --branch --untracked-files=all
git -C "<worktree>" status --short --ignored
git -C "<worktree>" rev-parse HEAD
# + Cleanup decision tree: still used / needed for review / unpushed state / detached commits / locks / services? If yes, retain.
# Remove leaves branch; do not delete branches here.
```

**3. Exact removal loop — spaces-safe, no `rm -rf`, no `--force`:**
```sh
repo="/repo"
prefix="$repo/.worktrees/"
git -C "$repo" worktree list --porcelain -z | while IFS= read -r -d '' line; do
  case "$line" in
    worktree\ *) path="${line#worktree }" ;;
    *) continue ;;
  esac
  case "$path" in
    "$prefix"* ) ;;
    *) continue ;;
  esac
  [ "$path" != "$repo" ] || continue
  [ "$path" != "$PWD" ] || { echo "skip current dir: $path" >&2; continue; }
  if [ -d "$path" ]; then
    git -C "$repo" worktree remove "$path"
  else
    echo "skip missing (possible offline volume, do not prune blindly): $path" >&2
  fi
done
```

**4. Prune only intentionally-removed registrations, same expiry:**
```sh
git -C "/repo" worktree prune --dry-run --verbose
# Review every entry — missing != removable if offline/locked.
git -C "/repo" worktree prune --verbose
```

**5. Verify:**
```sh
git -C "/repo" worktree list --porcelain -z
# Confirm removed paths gone; report retained checkouts/branches and why.
```

