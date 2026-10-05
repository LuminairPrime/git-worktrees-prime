No — not as planned. `git worktree move` explicitly **cannot move the main checkout**, and it **cannot move a worktree that contains submodules**. Both of your proposed operations will fail or corrupt registration if run that way. Here is what to do instead.

## 1. Checks to run first (both checkouts, in order)

```sh
# Inventory: absolute paths, branches, detached/locked state
git -C "<repo>" worktree list --porcelain -z

# Main checkout state
git -C "<old-main>" status --short --branch --untracked-files=all
git -C "<old-main>" status --short --ignored
git -C "<old-main>" rev-parse HEAD

# Linked task checkout state
git -C "<linked>" status --short --branch --untracked-files=all
git -C "<linked>" status --short --ignored
git -C "<linked>" rev-parse HEAD

# Submodule state inside the linked checkout (and main, if any)
git -C "<linked>" submodule status --recursive
git -C "<linked>" submodule foreach --recursive 'git status --short'

# Confirm no in-progress operation (merge/rebase/bisect/cherry-pick)
# and note the lock reason before touching anything:
git -C "<repo>" worktree list --porcelain | grep -A2 '^worktree' | grep -i lock
```

Do not proceed until: every checkout has a clean, identified state; you know each branch/HEAD and what untracked/ignored files exist (they will not survive a remove/re-add); submodules are clean or their changes are preserved; and no rebase/merge/bisect is in progress. Do **not** prune missing registrations while worktrees are live.

## 2. Main checkout — manual move + repair (never `git worktree move`)

```sh
# Stop services/editors/terminals whose cwd is inside it first
mv "<old-main>" "<new-main>"

# Reconnect every linked worktree to the moved main checkout
git -C "<new-main>" worktree repair "<linked>"   # repeat for each linked path

# If the main checkout itself is the only checkout, repair from any linked one:
# git -C "<linked>" worktree repair "<new-main>"

git -C "<new-main>" worktree list --porcelain -z   # verify new registration
git -C "<new-main>" status --short --branch
git -C "<new-main>" rev-parse HEAD
git -C "<linked>" status --short --branch          # linked checkout must work again

# If the main checkout has submodules, fix their gitdir pointers, then verify:
git -C "<new-main>" submodule status --recursive
```

Repair preserves branch, index, and state. Never "fix" a relocated checkout by pruning, deleting, or recreating it.

## 3. Linked checkout containing submodules — `git worktree move` is not supported

Preferred, supported path — remove and re-create at the new path (after the checks above; this loses untracked/ignored files and any uncommitted changes, so preserve them first):

```sh
git -C "<repo>" worktree remove "<linked>"
git -C "<repo>" worktree add "<new-linked>" "<task-branch>"
git -C "<new-linked>" submodule update --init --recursive
git -C "<new-linked>" status --short --branch
git -C "<new-linked>" submodule status --recursive
git -C "<repo>" worktree list --porcelain -z
```

If you must keep the exact directory (e.g. ignored files you won't copy), do a manual move instead:

```sh
mv "<linked>" "<new-linked>"
git -C "<new-main>" worktree repair "<new-linked>"
git -C "<new-linked>" submodule foreach --recursive 'git rev-parse --git-dir'   # pointers must resolve
git -C "<new-linked>" submodule status --recursive
git -C "<repo>" worktree list --porcelain -z
```

If submodule `.git` pointers are stale after the move (they hold absolute paths), reinitialize them without network loss of data — submodule repos persist in the main checkout's `.git/modules`:

```sh
git -C "<new-linked>" submodule deinit --force --all
git -C "<new-linked>" submodule update --init --recursive
```

(Only after confirming submodule working trees have no uncommitted changes you need.)

One more caution: submodules from different linked worktrees share one on-disk repository, so avoid checking out the same superproject/submodule combination concurrently while reorganizing.
