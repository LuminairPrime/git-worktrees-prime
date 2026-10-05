Plan — isolated worktree, no touch to colleague checkout:

1. Prove original checkout intact, record context:
`git status --short --branch`
`git stash list`
`git worktree list --porcelain`
`git branch --show-current; git rev-parse HEAD`

2. Get current base without pulling into colleague checkout:
`git fetch origin release/next`
`git rev-parse --verify release/next`

3. Verify requested path will be ignored in enclosing checkout:
`git rev-parse --show-toplevel`
`git rev-parse --path-format=absolute --git-path info/exclude`
`git check-ignore -q project/scratch-checkouts/normalize/`

4. Create task checkout + branch from base:
`git worktree add -b task/normalize project/scratch-checkouts/normalize release/next`

5. Verify new checkout registration and start state:
`git worktree list --porcelain`
`git -C project/scratch-checkouts/normalize branch --show-current`
`git -C project/scratch-checkouts/normalize rev-parse HEAD`
`git -C project/scratch-checkouts/normalize status --short --branch`
`git check-ignore -q project/scratch-checkouts/normalize/`

6. Edit only in task checkout — fix `normalize_label` to `strip()` surrounding whitespace and return lowercase.

7. Check + test only in task checkout:
`git -C project/scratch-checkouts/normalize status --short --branch`
`git -C project/scratch-checkouts/normalize diff`
Run project's check from `project/scratch-checkouts/normalize`.

8. Commit on task branch, no merge/push:
`git -C project/scratch-checkouts/normalize add <edited-file>`
`git -C project/scratch-checkouts/normalize commit -m "Fix normalize_label to strip and lowercase"`
`git -C project/scratch-checkouts/normalize log --oneline -2`
`git -C project/scratch-checkouts/normalize status --short --branch`

9. Leave ready for review, confirm original untouched:
`git worktree list --porcelain`
`git status --short --branch`
Retain `project/scratch-checkouts/normalize` on `task/normalize`. No merge, no push, no reset/clean/stash in original.

