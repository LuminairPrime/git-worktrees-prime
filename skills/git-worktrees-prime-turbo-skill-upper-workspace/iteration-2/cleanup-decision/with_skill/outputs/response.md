In `/tmp/skill-up-2831591834` I cannot verify `/repo/.worktrees/old-task`:

* `ls /repo`: `No such file or directory`
* current dir is not a git repo

Do not remove, delete, or prune until the checks below pass in the real repo. Run from a surviving checkout, not inside `/repo/.worktrees/old-task`.

Walkthrough per cleanup decision tree:

**1. Still in use?**
Retain if used by agent, editor, terminal, service, test. `cd` out before removal. Do not clean another worker's checkout.

**2. Still needed for review?**
If review can continue from integrated commits, checkout may go; retain branch/ref if needed.

**3. Would state disappear?**
Squash-merge makes this critical:
```sh
git -C "/repo/.worktrees/old-task" status --short --branch --untracked-files=all
git -C "/repo/.worktrees/old-task" status --short --ignored
git -C "/repo/.worktrees/old-task" rev-parse HEAD
```
Preserve valuable untracked/ignored files, detached commits, submodules outside deletion path. Clean status does not prove ignored/detached state is safe.

**4. Safe to remove checkout?**
```sh
git -C "/repo" worktree list --porcelain -z
```
Confirm canonical path, ownership, branch. Exclude primary checkout, current dir, parent, siblings. Only then:
```sh
git -C "/repo" worktree remove "/repo/.worktrees/old-task"
```
Do not `rm -rf` the directory.

**5. Safe to delete branch?**
Separate from 4. For squash, ancestry is broken, so expect failure:
```sh
git -C "/repo" merge-base --is-ancestor "<task-tip>" "<integration-ref>"
git -C "/repo" branch -d "<task-branch>"
```
`branch -d` checks upstream, not your integration target — success is not proof, failure is expected after squash. Verify replacement commits manually, e.g. diff of task changes vs target, `log`, `cherry`. Only if verified integrated/preserved or explicitly authorized for abandonment, and `branch -d` refuses for obsolete history, consider `branch -D` with authorization. Retain if pending review — closed PR alone is insufficient.

**6. Prune stale metadata?**
Prune removes registrations, not branches/dirs:
```sh
git -C "/repo" worktree prune --dry-run --verbose
git -C "/repo" worktree prune --verbose
```
Proceed only if every dry-run entry is intentionally removed. Missing dir may be offline volume — do not prune/unlock then. Use same expiry as dry-run.

**7. Verify:**
```sh
git -C "/repo" worktree list --porcelain -z
```
Check path gone, refs as intended. Report retained items + why.

Provide `worktree list --porcelain`, both `status` outputs, `rev-parse HEAD`, branch name, integration ref, and squash commit to authorize `remove` / `branch -D` / `prune`.

