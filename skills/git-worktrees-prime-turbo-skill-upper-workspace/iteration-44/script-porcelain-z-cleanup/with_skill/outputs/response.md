No repository was inspected — here is the script and its checks only.

## Checks, in order

1. **Repository answers.** `git -C /repo rev-parse --git-dir` must succeed (works for a checkout or a bare repo) before anything else runs.
2. **Inventory from Git, not from disk.** Enumerate with `git -C /repo worktree list --porcelain -z` and parse NUL-delimited fields. Never `ls`, `find`, or glob `/repo/.worktrees` — that both misses registrations and splits names containing spaces.
3. **Scope.** Keep only paths strictly under `/repo/.worktrees/`; exclude the primary checkout, `/repo` itself, `/repo/.worktrees` itself, and `$PWD`.
4. **Locked registrations.** A record with a `locked` field is skipped for removal *and* never pruned (it may be an offline volume, not a dead checkout).
5. **State checks on each existing directory** (in this order):
   - it really is a checkout of this repository (`git -C <path> rev-parse --git-dir`);
   - no non-ignored state would vanish (`git status --porcelain --untracked-files=all` empty) — the script never passes `--force`;
   - ignored/reproducible output is reported but does not block;
   - if the record is `detached`, its tip must be reachable from some ref (`git for-each-ref --contains=<sha>`), otherwise removal would orphan the commits.
6. **Removal goes through Git only.** `git -C /repo worktree remove "<path>"` for directories that still exist; never `rm -rf`. Directories already gone are left for the prune step. Branches are untouched.
7. **Prune dry run first.** `git -C /repo worktree prune --dry-run --verbose` — every line must be an intentionally removed checkout.
8. **Prune with exactly the reviewed options** (here: none — no `--expire` added between dry run and run).
9. **Verify.** Re-list worktrees and confirm the removed paths are gone while the task branches remain.

## The script

```bash
#!/usr/bin/env bash
#
# Remove linked task checkouts under /repo/.worktrees that still exist on
# disk, then prune stale registrations. Task names may contain spaces:
# everything is parsed from `git worktree list --porcelain -z`.

set -euo pipefail

repo=/repo
base="$repo/.worktrees"

# CHECK 1 -- /repo must answer as a Git repository (checkout or bare).
git -C "$repo" rev-parse --git-dir >/dev/null

# CHECK 2 -- inventory comes from Git's own registration list, NUL-delimited,
# so paths with spaces are never split. Never enumerate with ls/find/glob.

path= head= detached= lock_reason=

process() {
  local p=$1 h=$2 det=$3 why=$4

  # CHECK 3 -- only linked checkouts strictly under /repo/.worktrees/;
  # never the primary checkout, /repo, the tree root, or $PWD.
  case $p in
    "$base"/*) ;;
    *)         return 0 ;;
  esac
  case $p in
    "$repo"|"$base"|"$PWD") return 0 ;;
  esac

  # CHECK 4 -- a locked registration is never removed and never pruned.
  if [[ -n $why ]]; then
    printf 'SKIP locked   : %s (%s)\n' "$p" "$why" >&2
    return 0
  fi

  if [[ -d $p ]]; then
    # Directory still exists on disk -> remove it as a worktree.

    # CHECK 5a -- it must actually be a checkout of this repository.
    if ! git -C "$p" rev-parse --git-dir >/dev/null 2>&1; then
      printf 'SKIP not a git checkout: %s\n' "$p" >&2
      return 0
    fi

    # CHECK 5b -- non-ignored state would vanish with the directory:
    # refuse, and no --force appears anywhere below. Ignored (reproducible)
    # output is reported but does not block removal.
    if git -C "$p" status --porcelain --untracked-files=all | grep -q .; then
      printf 'SKIP dirty    : %s\n' "$p" >&2
      git -C "$p" status --short --untracked-files=all >&2
      return 0
    fi
    if git -C "$p" status --porcelain --untracked-files=all --ignored | grep -q '^!!'; then
      printf 'note ignored files go with the directory: %s\n' "$p" >&2
    fi

    # CHECK 5c -- a detached tip no ref reaches would be orphaned by removal.
    if [[ $det == yes && -n $h ]]; then
      if [[ -z $(git -C "$repo" for-each-ref --contains="$h" --format='%(refname)') ]]; then
        printf 'SKIP unreachable detached tip %s: %s\n' "$h" "$p" >&2
        return 0
      fi
    fi

    # CHECK 6 -- remove only through Git, never by deleting the directory.
    # Commits on a task branch survive removal; branches stay untouched.
    if git -C "$repo" worktree remove "$p"; then
      printf 'removed       : %s\n' "$p"
    else
      printf 'SKIP remove refused: %s\n' "$p" >&2
    fi
  else
    # Already gone -> its stale registration is left for the prune step.
    printf 'missing on disk (left for prune): %s\n' "$p"
  fi
  return 0
}

while IFS= read -r -d '' field; do
  case $field in
    'worktree '*)
      if [[ -n $path ]]; then process "$path" "$head" "$detached" "$lock_reason"; fi
      path=${field#worktree }
      head= detached= lock_reason= ;;
    'HEAD '*)   head=${field#HEAD } ;;
    'detached') detached=yes ;;
    'locked')   lock_reason='(no reason recorded)' ;;
    'locked '*) lock_reason=${field#locked } ;;
  esac
done < <(git -C "$repo" worktree list --porcelain -z)
if [[ -n $path ]]; then process "$path" "$head" "$detached" "$lock_reason"; fi

# CHECK 7 -- dry run. Review EVERY line: each entry must be a checkout that
# was intentionally removed above, never a locked or merely offline one.
printf '%s\n' '--- prune dry run ---'
git -C "$repo" worktree prune --dry-run --verbose

# CHECK 8 -- prune only after that review, with exactly the options just
# reviewed. This script adds no --expire or other expiry option at all.
if [[ ${PRUNE_CONFIRM:-no} == yes ]]; then
  git -C "$repo" worktree prune --verbose
else
  printf '%s\n' 'review the dry run above, then rerun with PRUNE_CONFIRM=yes' >&2
  exit 2
fi

# CHECK 9 -- verify: removed paths gone, registrations and branches intact.
git -C "$repo" worktree list --porcelain -z
git -C "$repo" branch --list
```

Run it once to get the removals plus the dry-run listing; after reviewing that listing, run `PRUNE_CONFIRM=yes bash script.sh` to prune. The second pass is idempotent — already-removed paths simply report as gone.
