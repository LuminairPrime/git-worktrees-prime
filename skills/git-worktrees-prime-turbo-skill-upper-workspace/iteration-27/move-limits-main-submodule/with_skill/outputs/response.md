No — do not run `git worktree move` for either case. It cannot move main or submodule-containing worktrees.

Common pre-checks, in order:

```sh
git -C "<repo>" worktree list --porcelain -z
git -C "<primary-root>" status --short --branch
git -C "<linked-worktree>" status --short --branch --untracked-files=all
git -C "<linked-worktree>" submodule status
```

Verify: canonical absolute paths, branch/detached HEAD + `HEAD` commit, uncommitted/untracked/ignored state, no ongoing merge/rebase/bisect, no agent/editor/terminal/service using the checkout, submodules/nested repos checked separately. Confirm destination path is unused. Leave the directory before moving.

1. Main checkout — filesystem move + repair, never `move`:

```sh
# <primary-root> = current main absolute path
mv "<primary-root>" "<new-primary-path>"
git -C "<new-primary-path>" worktree list --porcelain -z
git -C "<new-primary-path>" worktree repair "<linked-worktree>"
git -C "<new-primary-path>" worktree list --porcelain -z
```

Preserve `.git` and contents. Then repair each linked registration from the new main location and re-list to verify.

2. Linked checkout with submodules — filesystem move + repair, never `move`:

```sh
# multiple superproject checkouts are discouraged - confirm required
mv "<linked-worktree>" "<new-linked-path>"
git -C "<repo>" worktree repair "<new-linked-path>"
git -C "<repo>" worktree list --porcelain -z
git -C "<new-linked-path>" status --short --branch
git -C "<new-linked-path>" submodule status
git -C "<new-linked-path>" submodule foreach --recursive 'git status --short --branch'
```

Repair preserves branch/index/state. Do not prune, move, delete, or recreate the live checkout to fix registration.
