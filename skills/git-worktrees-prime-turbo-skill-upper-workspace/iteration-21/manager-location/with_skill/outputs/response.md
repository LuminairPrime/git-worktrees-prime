Place at `/repo/.worktrees/checkout-api`:

* No repo convention -> default is `<primary-root>/.worktrees/<task>`.
* `/repo` is main checkout, not bare, so sibling-dir rule does not apply.
* Use unused path, unique task name. Do not place inside another disposable worktree.

Before creating inside another checkout, verify ignore coverage:

1. `git -C "/repo" worktree list --porcelain -z` — confirm path unused and not inside a linked worktree.
2. Locate exclude: `git rev-parse --path-format=absolute --git-path info/exclude` — `.git` may be file.
3. Require exit 0: `git -C "/repo" check-ignore -q -- ".worktrees/checkout-api/"`
4. Verify again after creation with same `check-ignore`.
