Place at `/repo/.worktrees/checkout-api`:

* No repo convention -> use `<primary-root>/.worktrees/<task>`.
* Use unused path, unique descriptive name.
* Do not place inside another disposable worktree.

Before creating inside another checkout, verify destination is ignored:

1. Locate exclude file: `git rev-parse --path-format=absolute --git-path info/exclude` — `.git` may be a file.
2. From enclosing checkout run: `git check-ignore -q <relative-path>/` with trailing `/`, require exit `0`.
3. Verify again after creation.
