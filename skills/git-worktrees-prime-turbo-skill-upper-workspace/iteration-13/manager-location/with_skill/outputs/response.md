Place at `/repo/.worktrees/checkout-api`:

* Raw Git with no repo convention defaults to `<primary-root>/.worktrees/<task>`.
* Use unique task name and unused path. Do not place inside another disposable worktree.

Before creating inside another checkout, verify ignore coverage:

1. Locate exclude file: `git rev-parse --path-format=absolute --git-path info/exclude` from `/repo` — `.git` may be a file.
2. Ensure destination is ignored via `.gitignore` or local exclusion.
3. From enclosing checkout `/repo`, run: `git check-ignore -q .worktrees/checkout-api/` — require exit `0`.
4. Verify again after creation.
