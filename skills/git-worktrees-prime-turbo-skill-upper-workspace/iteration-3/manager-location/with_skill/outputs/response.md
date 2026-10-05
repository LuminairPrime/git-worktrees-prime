Place at `/repo/.worktrees/checkout-api`:

* No convention -> default for raw Git is `<primary-root>/.worktrees/<task>`.
* `/repo` is main checkout (not bare), so not sibling-dir case.
* Use unused path, do not nest inside another disposable worktree.

Before creating inside another checkout, verify ignore coverage:

1. Locate exclude: `git rev-parse --path-format=absolute --git-path info/exclude` — `.git` may be file.
2. From enclosing checkout, require exit 0:
   `git -C "<enclosing-checkout>" check-ignore -q -- "<selected-relative-path>/"`
3. Verify again after creation.

