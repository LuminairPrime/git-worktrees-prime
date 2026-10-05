Short answer: there's no `/repo` on this machine, so I can't run the checks for you — but yes, it's generally safe *if* each check below passes. Here are the checks in order, with the exact commands.

**1. Confirm ownership and identity of the checkout**
```sh
git -C /repo worktree list --porcelain -z
```
Confirm `/repo/.worktrees/old-task` is a linked worktree (not the primary checkout, not your current directory, not a sibling task), note its branch name and HEAD, and make sure you're the owner of it.

**2. Not still in use**
No agent, editor, terminal, test, or service still operating in that directory. Stop any task-owned processes and `cd` out of it first. Do not clean another worker's checkout.

**3. Nothing valuable would disappear**
```sh
git -C /repo/.worktrees/old-task status --short --branch --untracked-files=all
git -C /repo/.worktrees/old-task status --short --ignored
git -C /repo/.worktrees/old-task rev-parse HEAD
```
Tracked modifications, untracked/ignored files (secrets, local config, build products you actually need), detached commits, in-progress merges/rebases, and submodules/nested repos must all be accounted for. Clean status alone does not prove ignored files or detached commits are disposable.

**4. Verify integration (squash caveat — important)**

Squash merge breaks ancestry, so this will fail and prove nothing:
```sh
git -C /repo merge-base --is-ancestor <task-tip> <integration-ref>   # expect exit 1 after squash
```
Instead, verify the replacement commit landed on the integration target and the changes are present — e.g., find the squash commit on the integration branch (`git log --grep "<old-task>" <integration-ref>`), or confirm `git diff <task-tip> <integration-ref>` shows no remaining task changes. Note that `branch -d` may also check the branch's configured upstream rather than your intended integration target.

**5. Remove the checkout**
```sh
git -C /repo worktree remove /repo/.worktrees/old-task
```
Use `git worktree remove`, never `rm -rf` on the directory. Add `--force` only if a check above was resolved deliberately.

**6. Delete the branch (separately, only if earned)**
```sh
git -C /repo branch -d <task-branch>
```
Delete only if the work is verified integrated (step 4), preserved under another durable ref, or explicitly authorized for abandonment. If `-d` refuses because of the squash history, retain the branch until you've verified its history is obsolete and authorized — only then consider `-D`, which needs your explicit say-so.

**7. Prune — review the dry run first**
```sh
git -C /repo worktree prune --dry-run --verbose
```
Every listed entry must be an intentionally removed worktree. A missing directory may be an offline volume — do not prune just because it's unavailable. Then:
```sh
git -C /repo worktree prune --verbose
```
Pruning removes stale registrations only — not branches, not directories.

**8. Verify the result**
```sh
git -C /repo worktree list --porcelain -z
git -C /repo branch --list <task-branch>
```
Report what was removed vs. retained. A closed PR alone is not integration evidence, and an open PR means retain the branch for review.

If you run into a specific failure (e.g., `branch -d` refusing after the squash), paste the output and I can help interpret it.
