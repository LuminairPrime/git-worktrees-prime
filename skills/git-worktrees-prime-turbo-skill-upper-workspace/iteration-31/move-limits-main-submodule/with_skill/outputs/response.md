No. Do not run `git worktree move` for either.

`git worktree move` cannot move main or submodule-containing worktrees.

### Checks first - both checkouts

In order, from primary:

1. `git worktree list --porcelain -z` - confirm canonical absolute paths, branch/ref, ownership. Parse `-z`, do not eyeball.
2. `pwd` - confirm you are not inside a checkout to be moved.
3. For each checkout `<wt>`:
   `git -C "<wt>" status --short --branch`
   `git -C "<wt>" log -1 --oneline --decorate`
   `git -C "<wt>" rev-parse --absolute-git-dir --show-toplevel`
   `git -C "<wt>" submodule status`
4. Verify: no agent/editor/terminal/service/test using it, no rebase/merge/bisect/revert in progress, no tracked/untracked/ignored/detached state that would be lost. Check submodules/nested repos separately.
5. Verify destination path is unused and not inside another worktree.

### Main checkout - correct procedure

1. Stop task-owned processes, leave directory.
2. Filesystem move preserving `.git/` and contents, e.g.:
   `mv "<old-primary-root>" "<new-primary-root>"`
3. Reconnect registrations from new main:
   `git -C "<new-primary-root>" worktree repair "<new-primary-root>"`
   `git -C "<new-primary-root>" worktree repair "<linked-wt-current-absolute-path>"` for each linked checkout
4. Verify:
   `git -C "<new-primary-root>" worktree list --porcelain -z`

### Linked checkout with submodules - correct procedure

1. Same safety checks + record `submodule status`.
2. Filesystem move preserving `.git` file and contents:
   `mv "<old-linked>" "<new-linked>"`
3. Repair from main/bare:
   `git -C "<primary-root>" worktree repair "<new-linked>"`
4. Verify:
   `git -C "<primary-root>" worktree list --porcelain -z`
5. Then fix submodules separately in moved checkout:
   `git -C "<new-linked>" submodule status`
   `git -C "<new-linked>" status --short --branch`
   Do not use superproject `move/remove/prune` to fix submodule gitfiles.

