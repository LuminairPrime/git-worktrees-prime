Here is the script with its checks, in order.

## Pre-flight checks

1. `git` is available.
2. `/repo` exists and is a Git repository.
3. `/repo/.worktrees` exists.
4. Git version supports `--porcelain` (≥ 2.7).

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO="/repo"
WT_ROOT="${REPO}/.worktrees"

# --- Pre-flight checks ---------------------------------------------------

# 1. git is available
command -v git >/dev/null 2>&1 || { echo "git not found" >&2; exit 1; }

# 2. /repo exists and is a Git repository
[[ -d "${REPO}" ]] || { echo "${REPO} not found" >&2; exit 1; }
git -C "${REPO}" rev-parse --git-dir >/dev/null 2>&1 || {
  echo "${REPO} is not a git repository" >&2
  exit 1
}

# 3. /repo/.worktrees exists
[[ -d "${WT_ROOT}" ]] || { echo "${WT_ROOT} not found" >&2; exit 1; }

# 4. git supports --porcelain (2.7+)
git -C "${REPO}" worktree list --porcelain >/dev/null 2>&1 || {
  echo "git too old; --porcelain unsupported" >&2
  exit 1
}

# --- Main script ----------------------------------------------------------

# 1. Find linked task checkouts under /repo/.worktrees
#    and remove each one whose directory still exists on disk.
#    Task names may contain spaces, so parse --porcelain output
#    line-by-line with IFS= read -r and prefix matching.
git -C "${REPO}" worktree list --porcelain |
while IFS= read -r line; do
  case "$line" in
    "worktree "*)
      wt_path="${line#worktree }"
      case "$wt_path" in
        "${WT_ROOT}"/*)
          # 2. Remove each one whose directory still exists on disk.
          if [[ -d "$wt_path" ]]; then
            git -C "${REPO}" worktree remove --force "$wt_path"
          fi
          ;;
      esac
      ;;
  esac
done

# 3. Prune stale registrations (directories that no longer exist).
git -C "${REPO}" worktree prune
```

## Post-checks

1. No worktrees remain under `/repo/.worktrees`.
2. No stale registrations remain.

```bash
# 1. No worktrees remain under /repo/.worktrees
remaining="$(git -C "${REPO}" worktree list --porcelain |
  awk -v root="${WT_ROOT}/" '/^worktree / { p = substr($0, 10); if (p ~ "^" root) print p }')"
[[ -z "$remaining" ]] || { echo "Still present: $remaining" >&2; exit 1; }

# 2. No stale registrations remain
git -C "${REPO}" worktree list --porcelain |
  awk '/^worktree / { print substr($0, 10) }' |
while IFS= read -r p; do
  [[ -d "$p" ]] || { echo "Stale registration: $p" >&2; exit 1; }
done
```

**Notes**

- `--force` lets the removal succeed even with uncommitted changes; drop it if you want those to block instead.
- The `while` loop runs in a subshell (due to the pipe), so `exit` inside it only exits that subshell — the post-checks still run. If you need the main script to abort on removal failure, replace the pipe with a process substitution (`while ... done < <(git ...)`).
