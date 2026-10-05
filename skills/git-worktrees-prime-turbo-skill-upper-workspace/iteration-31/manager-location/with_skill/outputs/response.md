Place at `/repo/.worktrees/checkout-api`:

* No repo convention -> default is `<primary-root>/.worktrees/<task>`.
* Use unique task name + unused path.
* Don't place inside another disposable worktree.

Before creating inside another checkout, verify ignore coverage:

1. Locate exclude file: `git -C /repo rev-parse --path-format=absolute --git-path info/exclude` — `.git` may be a file.
2. From enclosing checkout `/repo`: `git check-ignore -q .worktrees/checkout-api/` — require exit `0`.
3. Verify again after creation.

See `references/raw-git-commands.md#creation` before `git worktree add`.

