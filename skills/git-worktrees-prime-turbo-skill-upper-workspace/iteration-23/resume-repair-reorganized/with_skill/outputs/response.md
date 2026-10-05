Resume in `case03/checkouts/adapter-current` — repair-before-work:

1. Read registration reference done. List current inventory:
```sh
git -C "case03/checkouts/adapter-current" worktree list --porcelain -z
```
Confirm owner/branch, note `adapter-old -> adapter-current` move.

2. Repair registration from main/bare repo, `<worktree>` = current absolute path:
```sh
git -C "<repo>" worktree repair "<absolute-path>/case03/checkouts/adapter-current"
git -C "<repo>" worktree list --porcelain -z
```
Verify `adapter-current` registered to `task/adapter`. Do not prune, move, delete, or recreate live checkout.

3. Establish starting state in same checkout only:
```sh
git -C "case03/checkouts/adapter-current" branch --show-current
git -C "case03/checkouts/adapter-current" status --short --branch --untracked-files=all
git -C "case03/checkouts/adapter-current" rev-parse HEAD
git -C "case03/checkouts/adapter-current" log --oneline -5
```
Expect `task/adapter`, preserve index/draft notes. Do not stash/reset. Abort if merge/rebase in progress.

4. Consume completed schema worker result:
```sh
cat worker-status.json
git show schema/prep:SCHEMA_VERSION
```
Proceed only if `schema/prep` = complete.

5. Finish `encode_record` in `case03/checkouts/adapter-current`: strip + lowercase `name`, include `enabled` as boolean, include `schema` from `SCHEMA_VERSION`. Edit function only, keep existing draft notes.

6. Validate with project check, run from task checkout:
```sh
git -C "case03/checkouts/adapter-current" status --short --branch
<project-check-from-checkout-instructions>
```
Require pass, no integration.

7. Commit on `task/adapter`:
```sh
git -C "case03/checkouts/adapter-current" add <adapter-file-only>
git -C "case03/checkouts/adapter-current" commit -m "<task-commit>"
git -C "case03/checkouts/adapter-current" status --short --branch
git -C "case03/checkouts/adapter-current" log --oneline -3
```

8. Leave ready for review, same checkout:
```sh
git -C "case03/checkouts/adapter-current" rev-parse --show-toplevel
git -C "case03/checkouts/adapter-current" branch --show-current
git worktree list --porcelain -z
```
Retain `case03/checkouts/adapter-current` on `task/adapter`. No merge/rebase to target, no push/publish, no `worktree remove/prune`, no branch delete.

