Place at `/repo/.worktrees/checkout-api`:

* Raw Git with no repo convention: `<primary-root>/.worktrees/<task>`.
* Use unused path, descriptive name. Do not place inside another disposable worktree.

Before creating inside another checkout, verify ignore coverage:

1. Locate exclude file: `git -C /repo rev-parse --path-format=absolute --git-path info/exclude` — `.git` may be a file.
2. From enclosing checkout: `git -C /repo check-ignore -q .worktrees/checkout-api/` — require exit `0` via `.gitignore` or local exclusion.
3. Verify again after creation.
