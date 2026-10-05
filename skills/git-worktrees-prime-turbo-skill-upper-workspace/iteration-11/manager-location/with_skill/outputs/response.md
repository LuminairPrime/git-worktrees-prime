Place at `/repo/.worktrees/checkout-api`:

* No repo convention -> default for raw Git is `<primary-root>/.worktrees/<task>`.
* `<primary-root>` is `/repo`. Not bare, so not sibling-dir case.
* Use unique task name and unused path; do not place inside another disposable worktree.

Before creating inside another checkout, verify ignore coverage:

1. Locate exclude file: `git rev-parse --path-format=absolute --git-path info/exclude` from `/repo` — `.git` may be a file.
2. Require ignored: run from enclosing checkout `/repo`:
   `git -C "/repo" check-ignore -q -- ".worktrees/checkout-api/"`
   Must exit `0` before creation.
3. Verify again after creation.
