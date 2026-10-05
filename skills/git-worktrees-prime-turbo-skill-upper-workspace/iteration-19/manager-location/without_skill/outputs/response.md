In this environment `/repo` does not exist - verified with `read:/repo`.

For raw `git worktree` with main checkout at `/repo`:

1. Placement: use sibling, not nested: `/checkout-api` i.e. `../checkout-api` relative to `/repo`.
   * Do not use `/repo/checkout-api` by default - it nests one checkout inside another.
2. Before creating inside another checkout, verify:
   * `git -C /repo rev-parse --git-dir` + `git worktree list --porcelain` - `/repo` is valid and path/branch `checkout-api` not already registered.
   * `git -C <parent> rev-parse --show-toplevel` - target is not inside another work-tree unintentionally. If you must nest, verify parent `.gitignore` ignores it, otherwise parent shows untracked noise/recursive scans.
   * target path does not already exist.

Command once `/repo` exists:

```sh
git -C /repo worktree add -b checkout-api /checkout-api
```
