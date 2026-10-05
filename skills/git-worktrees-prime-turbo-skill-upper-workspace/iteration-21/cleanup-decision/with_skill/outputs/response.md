In this environment `/repo/.worktrees/old-task` does not exist — `/repo` not found — so I did not remove/delete/prune anything.

Walkthrough for `/repo/.worktrees/old-task`, in order per cleanup decision tree:

1. **Still in use?** Confirm no agent/editor/terminal/service/test owns it. Leave the directory; run all removal from a surviving checkout, not from inside it.

2. **Still needed for review?** If review can continue from integrated commits, checkout may go; retain branch/ref if needed.

3. **State that disappears with directory?** From the task checkout:
```sh
git -C "/repo/.worktrees/old-task" status --short --branch --untracked-files=all
git -C "/repo/.worktrees/old-task" status --short --ignored
git -C "/repo/.worktrees/old-task" rev-parse HEAD
```
Clean status does not prove ignored files/detached commits safe. Check unfinished ops, submodules/nested repos separately. Preserve or get authorization to discard.

4. **Safe to remove checkout?** Verify canonical path + ownership:
```sh
git -C "/repo" worktree list --porcelain -z
```
Must be exactly that linked checkout — not primary, cwd, parent, or sibling task. Then only:
```sh
git -C "<surviving-checkout>" worktree remove "/repo/.worktrees/old-task"
```
Do not `rm -rf` the directory.

5. **Safe to delete branch?** Need your `<task-branch>` and `<integration-ref>`. Squash breaks ancestry, so expect this to fail:
```sh
git -C "/repo" merge-base --is-ancestor "<task-tip>" "<integration-ref>"
```
`branch -d` checks upstream, not your target — success is not integration evidence. Verify squash replacement commits + resulting diff. If `branch -d "<task-branch>"` refuses, retain it until obsolete history is verified safe + explicitly authorized, only then consider `branch -D`.

6. **Prune?** Only for intentionally removed registrations, after reviewing every entry:
```sh
git -C "/repo" worktree prune --dry-run --verbose
git -C "/repo" worktree prune --verbose
```
Same expiry options. Missing dir could be offline volume — do not prune that case.

7. **Verify:**
```sh
git -C "/repo" worktree list --porcelain -z
```
Check path gone, branch gone/retained.

To proceed I need: task branch name + tip, integration target ref, confirmation valuable state is preserved/abandon-authorized, and that the checkout is unused.

