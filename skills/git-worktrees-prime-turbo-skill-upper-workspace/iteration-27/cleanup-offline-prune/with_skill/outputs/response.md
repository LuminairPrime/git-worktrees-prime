Reclaim `case02/checkouts/completed` / `task/completed` only — no filesystem search, raw Git only:

1. Inventory — canonical paths, ownership:
```sh
git worktree list --porcelain -z
git -C "case02/checkouts/completed" rev-parse --show-toplevel
git -C "case02/checkouts/completed" rev-parse HEAD
git -C "case02/checkouts/completed" status --short --branch --untracked-files=all
git -C "case02/checkouts/completed" status --short --ignored
```
Check: `completed` is linked checkout, branch `task/completed`, not primary, not current dir. `review.db` appears in `--ignored` list.

2. Verify squash-integration — do not treat `branch -d` success as proof:
```sh
git rev-parse --verify "task/completed^{commit}"
git rev-parse --verify "release^{commit}"
git merge-base --is-ancestor "task/completed" "release"; echo $?
```
Expected: non-zero — squash/rebase breaks ancestry. Manually verify replacement commits/diff in `release` before proceeding. Retain branch regardless: review open on `task/completed`.

3. Preserve needed ignored state outside deletion path:
```sh
mkdir -p "<preserve-dir-outside-any-worktree>"
cp -p "case02/checkouts/completed/review.db" "<preserve-dir>/review.db"
ls -l "<preserve-dir>/review.db"
sha256sum "case02/checkouts/completed/review.db" "<preserve-dir>/review.db"
```

4. Leave checkout, remove only that checkout via manager:
```sh
cd "<primary-root-or-other-surviving-checkout>"
git worktree remove "case02/checkouts/completed"
```
No `rm -rf`, no `git worktree move`, no `-B`, no reset/clean.

5. Branch decision — retain:
Do NOT run `git branch -d task/completed` / `-D`. Open review needs it; squash tip is unmerged by ancestry and `-d` must refuse.

6. Stale registration decision — do NOT prune:
```sh
git worktree prune --dry-run --verbose
```
Expected entries: retired `scratch` (deleted, intentional) + `offline-worker` (missing only because share unmounted, colleague-owned, still in use). Per rule: prune only if every dry-run entry is intentional. Do NOT run `git worktree prune --verbose`, do NOT `lock/unlock` or prune the unavailable checkout.

7. Verify result:
```sh
git worktree list --porcelain -z
test ! -e "case02/checkouts/completed" && echo "completed removed"
git show-ref --verify --quiet "refs/heads/task/completed" && echo "task/completed retained"
ls -l "<preserve-dir>/review.db"
```

Report remains:
* Removed: checkout dir `case02/checkouts/completed` only.
* Retained: branch `task/completed` for open review; `review.db` copy at `<preserve-dir>/review.db`; `offline-worker` registration untouched; retired `scratch` stale registration intentionally left to protect `offline-worker` from global prune.

