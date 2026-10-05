No — do not run `git branch -D task/export` yet. `branch -d` refusal is expected after squash-merge.

Squash creates replacement commits, it does not preserve ancestry. `branch -d` / `merge-base --is-ancestor` will fail even when fully integrated, and `branch -d` success checks upstream, not your intended target — neither proves integration.

Run in order from a surviving checkout, `<repo>`:

```sh
# 1. Confirm checkout is gone and branch is not checked out elsewhere
git -C "<repo>" worktree list --porcelain -z
git -C "<repo>" branch --list "task/export"

# 2. Resolve current tips - fetch first if `main` must be current
git -C "<repo>" rev-parse --verify "task/export^{commit}"
git -C "<repo>" rev-parse --verify "main^{commit}"

# 3. Expected to fail after squash - exit 1 needs review, not deletion
git -C "<repo>" merge-base --is-ancestor "task/export" "main"

# 4. Verify replacement commits and resulting changes on `main`
git -C "<repo>" log --oneline main -20
git -C "<repo>" cherry main task/export
git -C "<repo>" diff main...task/export --stat
```

`cherry` should mark task commits `-` (patch already upstream), and `diff main...task/export` should show no unique unintegrated changes. Locate the squash commit in `log` and compare its `show` against the task diff. A closed PR alone is insufficient.

`git branch -D` is acceptable only when:

1. Work is verified integrated into the intended target, preserved under another durable ref, or explicitly authorized for abandonment.
2. Branch is task-owned, unused, not needed for pending review.
3. No state would disappear — checkout already removed, no detached commits / unfinished ops left.

Then:

```sh
git -C "<repo>" branch -D task/export
git -C "<repo>" branch --list "task/export"
git -C "<repo>" worktree list --porcelain -z
git -C "<repo>" worktree prune --dry-run --verbose
```

Prune only if dry-run lists only intentionally removed worktrees.

