No removal executed — target not found in this checkout:

* `/repo`: `No such file or directory`
* Current dir `/tmp/skill-up-4147509796` is not a git repo.

Walkthrough per cleanup decision tree — run in order from a surviving checkout:

1. **Still in use?** Leave dir, stop task-owned services. Do not clean another worker's checkout.
2. **Needed for review?** If review can continue from preserved commits, checkout may go; retain branch/ref.
3. **State that disappears with dir?** From the task checkout:
```sh
git -C "/repo/.worktrees/old-task" status --short --branch --untracked-files=all
git -C "/repo/.worktrees/old-task" status --short --ignored
git -C "/repo/.worktrees/old-task" rev-parse HEAD
```
Check detached commits, `MERGE_HEAD/rebase-merge/rebase-apply`, submodules/nested repos separately. Preserve or authorize discard.
4. **Safe to remove checkout?** Confirm canonical path vs inventory:
```sh
git -C "/repo" worktree list --porcelain -z
```
Must match exactly `/repo/.worktrees/old-task`, not primary, not cwd, not parent, not sibling task. Then only:
```sh
git -C "/repo" worktree remove "/repo/.worktrees/old-task"
```
Never `rm -rf` the directory.
5. **Safe to delete branch?** Squash breaks ancestry, so this will likely fail:
```sh
git -C "/repo" merge-base --is-ancestor "<task-tip>" "<integration-ref>"
git -C "/repo" branch -d "<task-branch>"
```
`branch -d` checks upstream, not your integration target — success is not integration evidence. For squash, verify replacement commits / resulting diff (e.g. patch-id / diff target vs tip). Only if verified integrated/preserved/authorized, and if `-d` refuses then explicitly authorized, consider `-D`.
6. **Prune?** Only for intentionally removed worktrees, after reviewing every entry:
```sh
git -C "/repo" worktree prune --dry-run --verbose
git -C "/repo" worktree prune --verbose
```
Do not prune a missing dir that is just offline/unmounted. Prune removes metadata only, not branches or live dirs.
7. **Verify:**
```sh
git -C "/repo" worktree list --porcelain -z
```

Provide the real `<task-branch>`, `<task-tip>`, and `<integration-ref>` and a repo path that exists here, and I can run steps 3-7.

