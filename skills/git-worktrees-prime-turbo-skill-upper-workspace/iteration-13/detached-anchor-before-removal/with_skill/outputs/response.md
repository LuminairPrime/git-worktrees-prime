No — do not `remove` yet. Detached `HEAD` commits are only reachable from that checkout. Removing it orphans them for GC.

In order, with `<repo>` = surviving checkout/bare repo, `<worktree>` = exact disposable path:

1. Confirm registration and ownership:
```sh
git -C "<repo>" worktree list --porcelain -z
```
Identify `<worktree>` canonical path; exclude primary, cwd, parent.

2. Inspect losable state — clean does not prove preserved:
```sh
git -C "<worktree>" status --short --branch --untracked-files=all
git -C "<worktree>" status --short --ignored
git -C "<worktree>" rev-parse HEAD
git -C "<worktree>" log --oneline -3
```

3. Anchor valuable tip to a durable ref before removal:
```sh
git -C "<worktree>" branch "<preservation-branch>" HEAD
git -C "<repo>" show-ref --verify --quiet "refs/heads/<preservation-branch>"
git -C "<repo>" log --oneline -3 "<preservation-branch>"
```

4. Leave `<worktree>`, then remove only via Git from `<repo>`:
```sh
git -C "<repo>" worktree remove "<worktree>"
```

5. Verify:
```sh
git -C "<repo>" worktree list --porcelain -z
git -C "<repo>" rev-parse --verify "<preservation-branch>^{commit}"
```
If integration claimed: `git -C "<repo>" merge-base --is-ancestor "<preservation-branch>" "<integration-ref>"` — exit 0 required.

Do not `rm -rf` the directory, do not `branch -d "<preservation-branch>"`, do not `worktree prune` unless `worktree prune --dry-run --verbose` shows only intentionally removed paths.

