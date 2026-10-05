Place at `/repo/.worktrees/checkout-api`:

* No repo convention -> default is `<primary-root>/.worktrees/<task>`.
* Use unused path, unique descriptive name.
* Don't place inside another disposable/linked worktree.

Before creating inside another checkout, verify ignore coverage:

1. From enclosing checkout, run `git check-ignore -q` on destination relative path with trailing `/` — requires exit `0`.
2. Locate exclude via `git rev-parse --path-format=absolute --git-path info/exclude` if not in `.gitignore` — `.git` may be a file.
3. Verify again after creation.
