No — do not run `git worktree move` for either case as planned:

`git worktree move` cannot move main or submodule-containing worktrees — `references/raw-git-commands.md:82-83`.

### 1. Checks first — both cases

Run from main checkout or bare repo, `<repo>` is existing checkout/bare repo:

```sh
git -C "<repo>" worktree list --porcelain -z
git -C "<primary-root>" rev-parse --show-toplevel
git -C "<primary-root>" status --short --branch --untracked-files=all
git -C "<primary-root>" rev-parse HEAD
git -C "<worktree>" status --short --branch --untracked-files=all
git -C "<worktree>" rev-parse HEAD
git -C "<worktree>" submodule status
```

Verify: canonical absolute paths, branch/detached + HEAD, owner/process still using it, no ongoing Git operation, untracked/ignored/nested-repo state, destination path unused. Do not prune/move/delete to fix registration.

### 2. Main checkout — correct procedure

`move` will refuse. Filesystem-relocate + repair:

```sh
# stop processes in checkout, leave directory
mv "<old-primary-root>" "<new-primary-root>"
git -C "<new-primary-root>" worktree repair "<new-linked-worktree-path>"
git -C "<new-primary-root>" worktree list --porcelain -z
git -C "<new-primary-root>" rev-parse --show-toplevel
git -C "<new-primary-root>" status --short --branch
```

Preserve `.git` and contents, repair with new absolute linked-worktree path, then verify inventory. Repair preserves branch/index/state.

### 3. Linked checkout with submodules — correct procedure

Do not `move`:

```sh
git -C "<repo>" worktree move "<worktree>" "<new-path>"
```

Retain in place. If relocation is mandatory: preserve valuable state outside deletion path, then remove via manager / `git worktree remove` and re-`add` at new location + re-init submodules — do not filesystem-delete, do not expect superproject move to handle submodules. Multiple superproject checkouts are discouraged — check submodule limitations first.

