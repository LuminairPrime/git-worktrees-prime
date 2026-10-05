`/repo` doesn't exist in this environment, so I can't run the checks against your actual repo — but here's the ordered walkthrough, straight from the worktrees skill. The path and branch name need to be confirmed at each step.

## 1. Confirm ownership and the exact checkout
```sh
git -C /repo worktree list --porcelain -z
```
- Verify `/repo/.worktrees/old-task` appears as a linked worktree, which branch it has checked out, and that it isn't the main checkout or your current working directory.
- Don't remove another worker's checkout, and leave the directory before removing it (no terminal/service/test using it).

## 2. Inspect for state that would disappear
```sh
git -C /repo/.worktrees/old-task status --short --branch --untracked-files=all
git -C /repo/.worktrees/old-task status --short --ignored
git -C /repo/.worktrees/old-task rev-parse HEAD
```
- Tracked modifications, untracked files, and ignored files all count. Ignored files are **not** preserved by removal — if any matter, copy them out first.
- Clean `status` alone does not prove ignored files or detached commits are safe to lose. Also check for in-progress operations (rebase/merge), submodules, and nested repos.

## 3. Verify the work really landed on the integration target
```sh
git -C /repo merge-base --is-ancestor <task-tip> <integration-ref>
```
- **Squash caveat:** a squash merge breaks ancestry — `<task-tip>` will typically *not* be an ancestor of the integration ref, so exit code will be nonzero. That's expected, but you must then verify the squashed commit's **changes** match what the branch contained (e.g. compare diffs of the integration commit vs. the task branch), and confirm the integration ref is current. A closed PR alone is not sufficient evidence.
- Record the integration commit SHA for your report.

## 4. Remove the checkout (only if checks 1–3 pass)
```sh
git -C /repo worktree remove /repo/.worktrees/old-task
```
- Use `git worktree remove`, never filesystem deletion. If it refuses due to modifications, that's a safeguard — resolve the cause, don't force.

## 5. Delete the branch (separate decision)
```sh
git -C /repo branch -d <task-branch>
```
- `branch -d` checks the branch against its **upstream**, not necessarily your intended integration target — success is not proof of integration, and with squash merges it will usually refuse. If it refuses, retain the branch until you've verified the obsolete history is safe and you're authorized to delete; only then consider `branch -D`.
- Retain the branch if a review is still pending.

## 6. Prune stale registrations
```sh
git -C /repo worktree prune --dry-run --verbose
git -C /repo worktree prune --verbose
```
- Review every dry-run entry first. Prune only if every entry is an intentionally removed worktree. Never prune a merely offline/unavailable checkout (e.g. unmounted volume) — that needs `worktree repair` or unlock instead.

## 7. Verify
```sh
git -C /repo worktree list --porcelain -z
git -C /repo branch --list <task-branch>
```
- Confirm the path is unregistered and the branch is gone (or deliberately retained). Report what was removed and what remains.

**Short answer:** yes — but only after each check passes. The squash merge means step 3's ancestry test will fail by design, so you need explicit verification that the squashed commit reproduces your branch's changes, and expect `branch -d` to refuse unless that history is confirmed safe to drop.
