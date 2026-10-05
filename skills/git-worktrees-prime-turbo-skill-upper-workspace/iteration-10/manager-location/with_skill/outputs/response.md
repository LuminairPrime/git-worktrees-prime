Place at `/repo/.worktrees/checkout-api`:

* No repo convention -> use `<primary-root>/.worktrees/<task>`.
* `/repo` is main checkout, so `<primary-root>` is `/repo`.
* Use unused path, unique descriptive name. Do not place inside another disposable worktree.

Before creating inside another checkout, verify ignore coverage:

1. Locate exclude file: `git rev-parse --path-format=absolute --git-path info/exclude` from enclosing checkout.
2. Ensure destination is ignored via `.gitignore` or local exclusion.
3. From enclosing checkout, run `git check-ignore -q` on destination's relative path with trailing `/` — require exit 0.
4. Verify again after creation.
