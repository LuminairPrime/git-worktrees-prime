## Placement

No repo location convention → use the skill's default: **`/repo/.worktrees/checkout-api`**

- Never inside another (disposable) worktree.
- Unique, descriptive task name; unused path.

## Verify before creating inside another checkout

The actual selected destination must be ignored (via `.gitignore` or a local exclusion) in the enclosing checkout:

1. **Locate the exclude file** (note `.git` may be a *file*, not a directory):
   ```sh
   git -C "<enclosing-checkout>" rev-parse --path-format=absolute --git-path info/exclude
   ```
2. **Check ignore coverage — must exit 0**, run from the enclosing checkout with a trailing `/` on the destination's relative path:
   ```sh
   git -C "<enclosing-checkout>" check-ignore -q -- ".worktrees/checkout-api/"
   ```
3. **Repeat the check after creation.**

If exit ≠ 0, add the destination to `.gitignore` or `info/exclude` first, and re-check.

## Pre-creation sanity checks

```sh
git -C /repo worktree list --porcelain -z
git -C /repo status --short --branch
git -C /repo rev-parse --verify "<base-ref>^{commit}"   # use the requested base; don't assume main/master/origin
```

## Creation

```sh
git -C /repo worktree add -b "<task-branch>" /repo/.worktrees/checkout-api "<base-ref>"
```
(use `-b` for a new branch; `-B` would reset an existing branch and needs explicit authorization)

## Verify afterwards

```sh
git -C /repo/.worktrees/checkout-api rev-parse --show-toplevel
git -C /repo/.worktrees/checkout-api status --short --branch
git -C /repo/.worktrees/checkout-api rev-parse HEAD
```
plus a repeat of the `check-ignore -q` step.

Also note: uncommitted changes do **not** carry over to a raw Git worktree — transfer any needed changes deliberately. And creation doesn't change your working directory; keep running commands with the explicit returned path.
