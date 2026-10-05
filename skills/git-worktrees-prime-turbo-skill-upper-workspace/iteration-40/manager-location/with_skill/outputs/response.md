**Where to place it**

Since you're using raw Git and there's no repo location convention, use the default: `<primary-root>/.worktrees/<task>`. With the main checkout at `/repo`, that means:

```
/repo/.worktrees/checkout-api
```

(If `/repo` were a bare repository instead, you'd use a sibling of the repo directory.) Also make sure the path is unique, descriptive, and not inside another disposable worktree.

**What to verify before creating inside another checkout**

Since `/repo/.worktrees/...` lives inside the main checkout, you must confirm the destination is ignored by Git *before* running `git worktree add`:

1. Locate the local exclude file (`.git` may be a file, so resolve it):
   ```sh
   git -C /repo rev-parse --path-format=absolute --git-path info/exclude
   ```
   Check ignore coverage via `.gitignore` or that exclude file.

2. Run the check from the enclosing checkout, with a trailing `/` on the destination's relative path, and require exit 0:
   ```sh
   git -C /repo check-ignore -q -- ".worktrees/checkout-api/"
   ```

3. Only proceed if it exits 0 (ignored). Then create with, e.g.:
   ```sh
   git -C /repo worktree add -b checkout-api /repo/.worktrees/checkout-api "<base-ref>"
   ```

4. Verify again after creation:
   - the same `check-ignore` still passes,
   - `git -C /repo/.worktrees/checkout-api rev-parse --show-toplevel`, `status --short --branch`, and `rev-parse HEAD` confirm the new checkout, branch, and starting commit.

If `check-ignore` doesn't return 0, don't create it there — add the path to `.gitignore`/exclude first or pick a location outside the checkout.
