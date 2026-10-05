Place at `/repo/.worktrees/checkout-api`:

* Raw Git, no repo convention: use `<primary-root>/.worktrees/<task>`.
* `/repo` is primary-root here. Use unused path + unique descriptive name. Do not place inside another disposable worktree.

Before creating inside another checkout, verify ignore coverage:

1. Locate exclude: `git rev-parse --path-format=absolute --git-path info/exclude` from enclosing checkout — `.git` may be a file.
2. Ensure destination ignored via `.gitignore` or local exclusion.
3. From enclosing checkout, require exit 0:
   `git -C /repo check-ignore -q -- .worktrees/checkout-api/`
4. Verify again after creation.
