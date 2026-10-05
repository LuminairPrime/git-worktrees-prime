Place it outside `/repo`:

* Default sibling: `/repo-checkout-api` / `/-checkout-api` parent with `-checkout-api` suffix, e.g. `git -C /repo worktree add /repo-checkout-api -b checkout-api`.
* Do not default to `/repo/checkout-api` or `/repo/.worktrees/checkout-api` - no repo convention allows that.

Before creating inside another checkout, verify with raw `git` in `/repo`:

1. `git rev-parse --show-toplevel --is-bare-repository --git-common-dir` - confirm main checkout root and not bare.
2. `git worktree list --porcelain` - target path unused, target branch not already checked out in another worktree.
3. `test -e <path>` - path must not exist / must be empty.
4. `git check-ignore -v <inside-path>` + `git status --porcelain --ignored` - nested path must be ignored, otherwise it pollutes `status`, gets caught by `add -A`, and can be deleted by `clean -fdx`.

