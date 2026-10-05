Place at `/repo/.worktrees/checkout-api` — raw Git default when no repo convention: `<primary-root>/.worktrees/<task>`.

Before creating inside another checkout, verify:

1. Not inside another disposable worktree.
2. Destination is ignored: locate exclude via `git rev-parse --path-format=absolute --git-path info/exclude` from `/repo`, ensure `.gitignore` or local exclude covers it.
3. Run `git check-ignore -q` from enclosing checkout on destination relative path with trailing `/`, require exit `0`.
4. Verify ignore again after creation.
