Place it at `/repo/.worktrees/checkout-api` — with raw Git and no repo location convention, the default is `<primary-root>/.worktrees/<task>` (for a bare repo, a sibling of the repo directory instead). Use a unique, descriptive path and a separate task branch (e.g. `checkout-api`); name the checkout path and branch separately. Don't place it inside another disposable worktree.

Before creating inside the main checkout (`/repo`), you must verify the destination is actually ignored:

1. Locate the exclude file: `git -C /repo rev-parse --path-format=absolute --git-path info/exclude` (note `.git` may be a file, not a directory).
2. Confirm ignore coverage — either `.gitignore` or that local exclude file covers it.
3. Run `git -C /repo check-ignore -q ".worktrees/checkout-api/"` (note the trailing `/` on the destination's relative path) and require exit code 0.
4. Verify again after creation.

Also read `references/raw-git-commands.md` (Creation section) before running `git worktree add`. If the destination isn't ignored and can't be made ignored, that setup is a blocker — don't silently create it inside the checkout. Want me to run these checks and create it?
