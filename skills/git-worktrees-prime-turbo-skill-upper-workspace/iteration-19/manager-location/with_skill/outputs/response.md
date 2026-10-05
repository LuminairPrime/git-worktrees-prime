Place at `/repo/.worktrees/checkout-api`:

* No repo convention -> use `<primary-root>/.worktrees/<task>`.
* Use unused path, unique descriptive name. Do not place inside another disposable worktree.

Before creating inside another checkout (`/repo`), verify ignore coverage:

1. Locate exclude file: `git rev-parse --path-format=absolute --git-path info/exclude` from `/repo` — `.git` may be a file.
2. Ensure destination is ignored via `.gitignore` or local exclusion.
3. From `/repo`: `git check-ignore -q .worktrees/checkout-api/` — require exit `0`. Note trailing `/`.
4. Verify again after creation.
