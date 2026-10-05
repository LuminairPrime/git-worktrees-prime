Place at `/repo/.worktrees/checkout-api`:

* No repo convention -> default raw-Git location is `<primary-root>/.worktrees/<task>`.
* Use unused path, unique descriptive name. Do not place inside another disposable worktree.

Before creating inside another checkout, verify ignore coverage:

1. Locate exclude via `git rev-parse --path-format=absolute --git-path info/exclude` — `.git` may be a file.
2. From enclosing checkout, require exit 0:
   `git -C /repo check-ignore -q -- .worktrees/checkout-api/`
   Note trailing `/` on relative path.
3. Verify again after creation.
