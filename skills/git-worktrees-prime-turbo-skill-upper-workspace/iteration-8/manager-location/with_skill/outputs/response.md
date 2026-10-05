Place at `/repo/.worktrees/checkout-api`:

* No repo convention → default raw-Git location: `<primary-root>/.worktrees/<task>`.
* Not bare, so not sibling-of-repo.
* Use unique task name + unused path; do not place inside another disposable worktree.

Before creating inside another checkout, verify ignore coverage:

1. Locate exclude: `git rev-parse --path-format=absolute --git-path info/exclude` — `.git` may be a file.
2. From enclosing checkout: `git -C "<enclosing-checkout>" check-ignore -q -- "<selected-relative-path>/"` — require exit `0`.
3. Verify again after creation.
