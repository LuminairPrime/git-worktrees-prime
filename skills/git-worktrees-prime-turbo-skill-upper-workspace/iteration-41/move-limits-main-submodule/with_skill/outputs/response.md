## Short answer: No — neither move can be done with `git worktree move`

Both of your targets are explicitly excluded from the command:

- **Main checkout** → `git worktree move` refuses: the main worktree cannot be moved this way.
- **Linked worktree containing submodules** → also refused ("working trees containing submodules cannot be moved or removed").

Both must instead be moved **manually with `mv` and then reconnected with `git worktree repair`**. Do not delete/recreate them, and do not run `git worktree prune` afterward thinking the registrations are stale — repair, not prune.

## Checks to run first (in order)

```sh
git --version                                   # move/repair must exist (repair is Git ≥ ~2.19; confirm with: git worktree -h)
git -C "<main>" worktree list --porcelain       # identify main (first entry) vs linked, exact paths, branches, "locked" entries
git -C "<main>" config core.worktree            # must be unset, or fix/migrate it (see extensions.worktreeConfig caveats)
git -C "<main>" config core.bare                # must be unset/false
git -C "<main>" status --short --branch         # no ongoing operation; also stop editors/builds/processes in the tree
git -C "<task>" status --short --branch         # same for the task checkout
git -C "<task>" submodule status --recursive    # enumerate submodules
cat "<task>/<submodule>/.git"                   # check whether the gitdir: path is relative or absolute
```

Also verify the new destination paths **do not exist yet** and are **not inside another worktree**, and note anything outside Git (hooks, IDE, CI, scripts) referencing the old absolute paths.

## Procedure 1 — main checkout (manual move + repair)

The main checkout's `.git` is a real directory, so it travels with the directory; what breaks is the reverse link stored in each **linked** worktree's `.git` file, which points at the old main path. Repair rewrites those:

```sh
mv /old/main /new/main
git -C /new/main worktree repair                # re-points all linked worktrees back to the new main location
git -C /new/main worktree list --porcelain      # verify all worktrees listed correctly
```

If the main checkout has submodules with absolute `gitdir:` paths (older clones), re-init them (`git -C /new/main submodule update --init --recursive`).

## Procedure 2 — linked task worktree with submodules (manual move + repair)

The submodule gitdirs live under the main repo (`.git/modules/...` / `.git/worktrees/<id>/modules/...`) and each has a `core.worktree` pointing back at the **old** worktree path. Cleanest sequence is to deinit first, so no stale submodule paths survive:

```sh
git -C /old/task submodule deinit -f --all      # recommended: avoids stale core.worktree/gitdir paths
mv /old/task /new/task
git -C /new/main worktree repair /new/task      # run from the main repo, with the NEW absolute path
git -C /new/task submodule update --init --recursive
git -C /new/main worktree list --porcelain      # verify registration
git -C /new/task status --short --branch        # verify checkout works
git -C /new/task submodule status --recursive   # verify submodules
```

If you skip the deinit, repair still reconnects the worktree itself, but you must then fix every submodule's `core.worktree` and any absolute `gitdir:` lines by hand — which is why deinit → move → repair → re-init is the safer path.

## If you move both

Order doesn't matter as long as repair runs last, from the new main location:

```sh
mv /old/main /new/main
mv /old/task /new/task
git -C /new/main worktree repair /new/task      # fixes both directions for the task worktree in one pass
git -C /new/main worktree repair                # fixes any other (unmoved) linked worktrees
git -C /new/main worktree list --porcelain      # final verification
```

One nuance: repair with an explicit path is what you want for the *moved* linked worktree — bare `git worktree repair` alone can't find a worktree whose path also changed, because its recorded location is the old one.
