In `project/` - colleague-owned, dirty - inspect only, do not modify:

1. `git -C project status --short --branch`
2. `git -C project worktree list --porcelain`
3. `git -C project rev-parse --show-toplevel`
4. `git -C project rev-parse --path-format=absolute --git-path info/exclude`
5. `git -C project check-ignore -q scratch-checkouts/normalize/`
   - If exit !=0, add `scratch-checkouts/` to that `info/exclude` file, then re-run check, require exit 0. Do not edit tracked `.gitignore`, `stash`, `reset`, `clean`, or `pull` in this checkout.

Establish base, no writes to old checkout:

6. `git -C project fetch origin release/next`
7. `git -C project rev-parse --verify origin/release/next`

Create isolated checkout, exact path/branch/base:

8. `git -C project worktree add -b task/normalize scratch-checkouts/normalize origin/release/next`

Verify new checkout `project/scratch-checkouts/normalize`:

9. `git -C project/scratch-checkouts/normalize rev-parse --abbrev-ref HEAD`
10. `git -C project/scratch-checkouts/normalize log -1 --oneline`
11. `git worktree list --porcelain`
12. `git -C project check-ignore -v scratch-checkouts/normalize/`

Fix in new checkout only:

13. `grep -rn "normalize_label" project/scratch-checkouts/normalize`
14. Edit that definition to: `return text.strip().lower()`
15. `git -C project/scratch-checkouts/normalize diff`

Run repo-documented check in new checkout:

16. Inspect `README/CONTRIBUTING/package.json/pyproject.toml/Makefile` in new checkout for `check/test/lint` command
17. Run that check in `project/scratch-checkouts/normalize`, require pass

Commit on `task/normalize`, leave for review - no merge/push:

18. `git -C project/scratch-checkouts/normalize add <edited-file>`
19. `git -C project/scratch-checkouts/normalize status --short --branch`
20. `git -C project/scratch-checkouts/normalize commit -m "Fix normalize_label to strip and lowercase"`
21. `git -C project/scratch-checkouts/normalize log -1 --stat`
22. `git -C project/scratch-checkouts/normalize status --short --branch`
23. `git worktree list --porcelain`

Retained: checkout `project/scratch-checkouts/normalize`, branch `task/normalize`, base `origin/release/next`. No `merge`, `push`, `worktree remove`, `branch -d`, or `prune`.

