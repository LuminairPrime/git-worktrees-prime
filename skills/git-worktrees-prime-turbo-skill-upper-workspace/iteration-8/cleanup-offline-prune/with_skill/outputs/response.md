Per `references/raw-git-commands.md:42-62` cleanup, in order — do not `rm -rf`, do not delete branch, do not prune:

1. Inventory — confirm canonical path/branch/owner:
```sh
git -C "<primary-root>" worktree list --porcelain -z
git worktree list --porcelain
```
Require `case02/checkouts/completed` == registered absolute `<worktree>` on `task/completed`, not primary, not cwd, not parent, not sibling task. Leave that directory; run removal from surviving checkout.

2. State that would disappear with directory:
```sh
git -C "case02/checkouts/completed" status --short --branch --untracked-files=all
git -C "case02/checkouts/completed" status --short --ignored
git -C "case02/checkouts/completed" rev-parse HEAD
git -C "case02/checkouts/completed" submodule status
```
Expect ignored `review.db` visible only in second command. Save tip as `<task-tip>`.

3. Preserve reviewer need outside deletion path before removal:
```sh
mkdir -p "<preserved-dir-outside-deletion-path>"
cp -p "case02/checkouts/completed/review.db" "<preserved-dir-outside-deletion-path>/review.db"
ls -l "<preserved-dir-outside-deletion-path>/review.db"
```

4. Branch-retention check — do not delete:
```sh
git -C "<primary-root>" show-ref --verify --quiet "refs/heads/task/completed"
git -C "<primary-root>" merge-base --is-ancestor "<task-tip>" "release"; echo $?
```
Squash-integration breaks ancestry — expect non-zero. Regardless, review remains open on `task/completed`: checkout may go, ref must stay. Do NOT run `branch -d/-D task/completed`.

5. Remove only exact checkout via manager:
```sh
git -C "<primary-root>" worktree remove "<absolute-path-to-case02/checkouts/completed>"
```

6. Verify removal + retention:
```sh
git -C "<primary-root>" worktree list --porcelain -z
test ! -e "case02/checkouts/completed" && echo "checkout gone"
git -C "<primary-root>" show-ref --verify "refs/heads/task/completed"
git -C "<primary-root>" rev-parse --verify "task/completed^{commit}"
```

7. Stale-metadata dry-run only:
```sh
git -C "<primary-root>" worktree prune --dry-run --verbose
```
Expected: `scratch` missing/deleted + `offline-worker` missing/unmounted. Do NOT run `worktree prune --verbose` / `unlock`: every dry-run entry is not intentionally removed — offline share is colleague-owned, still in use. Pruning would discard live registration.

Report remains:
- Removed: `case02/checkouts/completed` checkout only.
- Retained: branch `task/completed` at `<task-tip>` for open review; `review.db` copy at `<preserved-dir-outside-deletion-path>/review.db`; `offline-worker` registration (unmounted, colleague-owned); stale `scratch` registration (prune deferred because global prune would also drop offline-worker).

