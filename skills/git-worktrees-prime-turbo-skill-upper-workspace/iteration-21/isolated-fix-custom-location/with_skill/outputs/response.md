In `project/` on `release/next`, new checkout `project/scratch-checkouts/normalize`, branch `task/normalize`. No integration/merging requested - leave for review.

Pre-checks in colleague's checkout - do not modify:
1. `git -C project worktree list --porcelain -z`
2. `git -C project status --short --branch` - confirm unrelated notes/modified + untracked draft, leave intact. No `stash/reset/clean/pull`.
3. `git -C project fetch origin release/next`
4. `git -C project rev-parse --verify "release/next^{commit}"`
5. `git -C project rev-parse --path-format=absolute --git-path info/exclude`
6. `git -C project check-ignore -q -- scratch-checkouts/normalize/` - require exit 0, else add ignore before proceeding.

Create:
7. `git -C project worktree add -b task/normalize scratch-checkouts/normalize release/next` - use `-b`, not `-B`.

Verify new checkout:
8. `git -C project/scratch-checkouts/normalize rev-parse --show-toplevel`
9. `git -C project/scratch-checkouts/normalize status --short --branch`
10. `git -C project/scratch-checkouts/normalize rev-parse HEAD` - must equal `release/next` tip.
11. `git -C project check-ignore -q -- scratch-checkouts/normalize/` - require exit 0 again.

Develop in `project/scratch-checkouts/normalize` only:
12. Edit `normalize_label` to `return label.strip().lower()`.
13. Run documented check from task checkout, e.g. `pytest/make check/npm test` + targeted `strip/lowercase` assertion.
14. `git -C project/scratch-checkouts/normalize status --short --branch --untracked-files=all`
15. `git -C project/scratch-checkouts/normalize add <task-files-only>`
16. `git -C project/scratch-checkouts/normalize commit -m "Fix normalize_label to strip and lowercase"`

Ready for review - retain, do not integrate:
17. `git -C project/scratch-checkouts/normalize log --oneline -3`
18. `git -C project worktree list --porcelain -z`
19. Retain checkout + `task/normalize`. No `merge/rebase/push`, no `worktree remove/branch -d/prune`.

