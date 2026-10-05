# Raw Git commands

Apply the main skill's ownership, preservation, and safety checks. Substitute all placeholders. Run only commands for the selected operation, including its prerequisite checks.

## Creation

Inspect the source and selected base:

```sh
git -C "<repo>" worktree list --porcelain -z
# Only when <repo> is a checkout, not a bare repository.
git -C "<repo>" status --short --branch
git -C "<repo>" rev-parse --verify "<base-ref>^{commit}"

# Only for a destination inside another checkout; require exit 0 before creation.
git -C "<enclosing-checkout>" check-ignore -q -- "<selected-relative-path>/"
```

Choose one creation alternative:

```sh
# New branch, explicitly based on the selected commit/ref.
git -C "<repo>" worktree add -b "<task-branch>" "<worktree>" "<base-ref>"

# Alternative: continue an existing branch that is not checked out elsewhere.
# Require exit 0; do not let a missing local branch resolve to a remote branch.
git -C "<repo>" show-ref --verify --quiet "refs/heads/<task-branch>"
git -C "<repo>" worktree add "<worktree>" "<task-branch>"

# Alternative: disposable inspection of a specific commit.
git -C "<repo>" worktree add --detach "<worktree>" "<commit>"
```

Verify the resulting checkout and repeat any required ignore check:

```sh
git -C "<worktree>" rev-parse --show-toplevel
git -C "<worktree>" status --short --branch
git -C "<worktree>" rev-parse HEAD
```

## Cleanup

```sh
# Clean status does not establish preservation of ignored files or detached commits.
git -C "<worktree>" status --short --branch --untracked-files=all
git -C "<worktree>" status --short --ignored
git -C "<worktree>" rev-parse HEAD

# Exit 0 proves this tip is an ancestor of this target. Other outcomes need review.
git -C "<repo>" merge-base --is-ancestor "<task-tip>" "<integration-ref>"

# Run from a surviving checkout or bare repository after the checks above.
# Remove only if the cleanup decision tree permits checkout removal.
git -C "<repo>" worktree remove "<worktree>"
# Separately, delete the branch only if the branch-deletion conditions are met.
git -C "<repo>" branch -d "<task-branch>"
git -C "<repo>" worktree list --porcelain -z

# Only for intentionally removed worktrees; review every dry-run entry before pruning.
git -C "<repo>" worktree prune --dry-run --verbose
git -C "<repo>" worktree prune --verbose
```

## Registration

Repair a relocated live checkout, lock one before its storage goes offline,
or move a linked checkout. Run from the main checkout or bare repository;
`<worktree>` is the checkout's current absolute path.

```sh
git -C "<repo>" worktree list --porcelain -z
git -C "<repo>" worktree repair "<worktree>"
git -C "<repo>" worktree list --porcelain -z

# Before storage goes offline; the reason flag precedes the path.
# Read the reason before unlocking; never prune or unlock a merely
# unavailable checkout.
git -C "<repo>" worktree lock --reason "<why-offline>" "<worktree>"
git -C "<repo>" worktree unlock "<worktree>"

# Linked checkouts only; cannot move main or submodule-containing worktrees.
git -C "<repo>" worktree move "<worktree>" "<new-path>"
```
