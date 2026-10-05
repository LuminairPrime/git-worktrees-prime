Place at `/repo/.worktrees/checkout-api`:
raw Git with no repo convention -> `<primary-root>/.worktrees/<task>`.

Before creating inside another checkout:
1. Don't place inside another disposable worktree. Use unused path.
2. Ensure destination is ignored via `.gitignore` or local exclude.
3. Locate exclude with `git rev-parse --path-format=absolute --git-path info/exclude` from enclosing checkout.
4. Run `git check-ignore -q <relative-path>/` from enclosing checkout - require exit 0.
5. Verify again after creation.
