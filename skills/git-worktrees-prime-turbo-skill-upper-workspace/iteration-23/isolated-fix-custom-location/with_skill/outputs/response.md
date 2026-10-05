In `project` checkout — do not modify it, no pull/reset/clean:

1. Record ownership / starting state:
```bash
pwd
git branch --show-current
git rev-parse HEAD
git status --short --branch
git stash list
git ls-files --others --exclude-standard
git worktree list --porcelain
git branch --list "task/normalize"
```
Checks: current branch is colleague's, `status` shows unrelated notes modified + untracked draft, `task/normalize` not already listed in any checkout.

2. Resolve primary root and base `release/next`, no pull into this checkout:
```bash
git rev-parse --show-toplevel
git fetch origin release/next
git rev-parse --verify --quiet release/next
git log --oneline -1 release/next
```
Check: `release/next` resolves, that commit is intended base.

3. Ensure requested path is ignored before creation:
```bash
git rev-parse --path-format=absolute --git-path info/exclude
git check-ignore -q scratch-checkouts/normalize/
```
If exit !=0, add local-only exclusion, do not touch tracked `.gitignore` in colleague's checkout:
```bash
printf 'scratch-checkouts/\n' >> "$(git rev-parse --path-format=absolute --git-path info/exclude)"
git check-ignore -q scratch-checkouts/normalize/
```
Check: exit 0.

4. Create separate checkout, new branch from base:
```bash
git worktree add -b task/normalize scratch-checkouts/normalize release/next
```
Do not use `-B`, do not stash/copy uncommitted notes/draft.

5. Verify registration / starting state:
```bash
git worktree list --porcelain
git -C scratch-checkouts/normalize branch --show-current
git -C scratch-checkouts/normalize rev-parse HEAD
git -C scratch-checkouts/normalize status --short --branch
git -C scratch-checkouts/normalize log --oneline -1
git check-ignore -q scratch-checkouts/normalize/
```
Checks: path `project/scratch-checkouts/normalize`, branch `task/normalize`, `HEAD==release/next`, clean, ignore still exit 0.

6. Fix in task checkout only:
```bash
# edit file defining normalize_label to:
# return text.strip().lower()
```
Keep all work under `scratch-checkouts/normalize`.

7. Run project's documented check from task checkout:
```bash
git -C scratch-checkouts/normalize status --short
# run check as defined by repo, e.g.:
git -C scratch-checkouts/normalize test
```
Check: passes.

8. Commit on task branch:
```bash
git -C scratch-checkouts/normalize add <file-containing-normalize_label>
git -C scratch-checkouts/normalize status --short
git -C scratch-checkouts/normalize commit -m "Fix normalize_label to strip whitespace and lowercase"
git -C scratch-checkouts/normalize log --oneline -2
git -C scratch-checkouts/normalize status --short --branch
```
Check: `task/normalize` ahead of `release/next` by 1.

9. Leave ready for review, prove original intact, no integration:
```bash
git status --short --branch
git worktree list --porcelain
```
Checks: colleague's modified notes + untracked draft still present, both checkouts registered. Do not run `merge/rebase/push/pr create/worktree remove/prune/branch -d/-D`.

