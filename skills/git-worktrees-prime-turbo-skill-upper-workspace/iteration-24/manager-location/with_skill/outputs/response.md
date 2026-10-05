Place at `/repo/.worktrees/checkout-api`:
* Raw Git default with no repo convention is `<primary-root>/.worktrees/<task>`.
* Use unused path, descriptive name. Don't nest inside another disposable worktree.

Before creating inside another checkout, verify ignore coverage:
1. Locate exclude file: `git rev-parse --path-format=absolute --git-path info/exclude` from enclosing checkout.
2. Require ignored: `git -C "<enclosing-checkout>" check-ignore -q -- "<selected-relative-path>/"` must exit `0`.
3. Verify again after creation with `git -C "<worktree>" rev-parse --show-toplevel` + repeat ignore check.
