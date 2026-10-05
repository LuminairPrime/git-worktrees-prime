Per `references/raw-git-commands.md:42-63`: parse `list --porcelain -z`, use `worktree remove`, then dry-run/review/prune with identical expiry options.

Checks + script in order:

1. Verify repo and inventory — authority is Git, not `ls`/`find`:
```sh
git -C "/repo" rev-parse --show-toplevel
git -C "/repo" worktree list --porcelain -z
pwd # must not equal any removal target
```

2. Per candidate under `/repo/.worktrees`: verify canonical path/ownership from step 1, branch/`HEAD`, in-use, and preservation:
```sh
git -C "<candidate>" status --short --branch --untracked-files=all
git -C "<candidate>" status --short --ignored
git -C "<candidate>" rev-parse HEAD
# Retain if in-use, needed for review, or valuable state would be lost.
# Never `rm -rf`, never `--force` without resolving cause.
```

3. Remove only existing linked checkouts under that base:
```bash
set -eu
repo="/repo"
base="/repo/.worktrees"
git -C "$repo" worktree list --porcelain -z |
while IFS= read -r -d '' field; do
  case "$field" in worktree\ *) wt="${field#worktree }";; *) continue;; esac
  case "$wt" in "$base"/*) ;; *) continue;; esac
  [ -d "$wt" ] || continue
  [ "$wt" != "$PWD" ] || { echo "skip current dir: $wt" >&2; continue; }
  git -C "$repo" worktree remove "$wt"
done
```
NUL-delimited + quoted `"$wt"` handles spaces. Removes checkouts only; branches remain.

4. Prune only intentionally-removed registrations, same options as dry-run:
```sh
git -C "/repo" worktree prune --dry-run --verbose
# Review every entry: must all be intentionally removed, not offline/moved.
git -C "/repo" worktree prune --verbose
```

5. Verify result:
```sh
git -C "/repo" worktree list --porcelain -z
```
