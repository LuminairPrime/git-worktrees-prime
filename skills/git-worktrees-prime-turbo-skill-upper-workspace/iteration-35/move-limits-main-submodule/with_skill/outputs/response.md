No — you should **not** run `git worktree move` for either of these targets. Git refuses both cases:

- `git worktree move` only works on **linked** worktrees; it cannot move the **main** (primary) checkout.
- It also refuses any worktree that **contains submodules**.

So each needs a different, manual-then-repair procedure. Run this in order:

## 1. Checks first (both cases)

```sh
# Snapshot current registrations and state before touching anything
git -C "<main>" worktree list --porcelain -z
git -C "<main>" status --short --branch

git -C "<linked>" status --short --branch --untracked-files=all
git -C "<linked>" rev-parse HEAD

# In-progress operations would be corrupted by a move — must be empty
git -C "<linked>" rev-parse MERGE_HEAD REBASE_HEAD 2>/dev/null

# Enumerate submodules; note commits/state — uncommitted submodule
# changes live only inside the directories, not in any ref
git -C "<linked>" submodule status --recursive

# Record the old absolute paths; you need them in the submodule fixup below
pwd
```

Verify ownership (no agent/editor/service is actively using either checkout), and stop task-owned processes. If storage might go offline during the move, lock first:

```sh
git -C "<main>" worktree lock --reason "reorganization" "<linked>"
```

## 2. Main checkout → filesystem move + repair

```sh
mv "<old-main>" "<new-main>"
git -C "<new-main>" worktree repair          # no args: repair all links to the old main path
git -C "<new-main>" worktree list --porcelain -z
git -C "<new-main>" status --short --branch
```

`repair` reconnects it to its linked worktrees and rewrites the registration metadata; your branch, index, and working tree are preserved. Do **not** `prune` or recreate — prune would drop the live linked registrations.

## 3. Linked task checkout with submodules → filesystem move + repair + submodule fixup

```sh
mv "<old-linked>" "<new-linked>"
git -C "<new-main>" worktree repair "<new-linked>"
```

`worktree repair` fixes the worktree's own registration and its `.git` gitfile, but **not** the submodule administrative files, which still hold the old absolute paths. Fix them per submodule:

```sh
git -C "<new-linked>" submodule foreach --recursive '
  stale=$(sed "s/^gitdir: //" "$sm_path/.git")
  new=${stale/"<old-linked-abs-path>"/"$toplevel"}
  printf "gitdir: %s\n" "$new" > "$sm_path/.git"
  git --git-dir="$new" config core.worktree "$toplevel/$sm_path"
  printf "%s\n" "$toplevel/$sm_path/.git" > "$new/gitdir"
'

# Verify
git -C "<new-linked>" submodule status --recursive
git -C "<new-linked>" status --short --branch
git -C "<new-main>" worktree list --porcelain -z
```

(Substitute the real old absolute path. If submodules exist in the *main* checkout too, run the same `foreach` fixup there with `<old-main>`.)

## 4. If the storage later goes offline for long

`git gc` can auto-prune missing worktree registrations (`gc.worktreePruneExpire`). Repair promptly, and keep the `--reason` lock until the checkout is stable; unlock only after confirming the reasons with `git worktree list --porcelain -z`.

Note: for a *plain* linked checkout (no submodules), the supported command would simply be `git -C "<main>" worktree move "<linked>" "<new-linked>"` — your linked checkout doesn't qualify because of its submodules.
