`/repo` doesn't exist in this environment, so here's the guidance rather than an executed setup (give me a real path and I'll run it).

## Where to place it

With no repository location convention, raw Git placement defaults to `<primary-root>/.worktrees/<task>`:

```
/repo/.worktrees/checkout-api
```

Rules that apply:
- Use a unique, descriptive task name (`checkout-api` qualifies) and a path that isn't already in use — confirm against `git -C /repo worktree list --porcelain -z`.
- Never place a worktree inside another *disposable* worktree. Inside the **primary** checkout (`/repo`) is fine; nested inside e.g. `/repo/.worktrees/other-task` is not.
- (If the repo were bare instead of a checkout at `/repo`, the default would be a sibling of the repo directory, not inside it.)

## What to verify before creating inside another checkout

Because `/repo/.worktrees/checkout-api` sits inside the `/repo` checkout, that destination must be ignored so it doesn't show up as untracked content:

1. **Add an ignore rule** covering it — either `.gitignore` in `/repo` or the local exclude file. Locate the exclude file with:
   ```sh
   git -C /repo rev-parse --path-format=absolute --git-path info/exclude
   ```
   (resolve it this way because `.git` may be a file, not a directory).
2. **Require the ignore check to succeed** — run from the enclosing checkout, with a trailing `/` on the destination's relative path, and require exit 0:
   ```sh
   git -C /repo check-ignore -q -- ".worktrees/checkout-api/"
   ```
3. **Verify again after creation** — repeat the same `check-ignore` once the worktree exists.

## Creation sequence (raw Git)

```sh
# Pre-checks
git -C /repo worktree list --porcelain -z
git -C /repo status --short --branch
git -C /repo rev-parse --verify "<base-ref>^{commit}"   # resolve the intended base
git -C /repo check-ignore -q -- ".worktrees/checkout-api/"   # must exit 0

# Create with a NEW task branch (use -b, never -B unless resetting a branch is authorized)
git -C /repo worktree add -b "checkout-api" "/repo/.worktrees/checkout-api" "<base-ref>"

# Verify the result
git -C /repo/.worktrees/checkout-api rev-parse --show-toplevel
git -C /repo/.worktrees/checkout-api status --short --branch
git -C /repo/.worktrees/checkout-api rev-parse HEAD
git -C /repo check-ignore -q -- ".worktrees/checkout-api/"   # re-check ignore
```

One caution on the base: don't assume `main`, `master`, `origin`, or current `HEAD` is the right starting point — determine the repository's actual integration target first, and fetch the remote first if a current remote base is required.
