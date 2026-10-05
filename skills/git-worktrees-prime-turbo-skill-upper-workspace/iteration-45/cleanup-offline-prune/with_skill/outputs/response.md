## Plan — exact commands and checks, in order

`<primary-root>` = main checkout (or bare repo admin dir); `<completed>` = absolute path of `case02/checkouts/completed`; `<offline>` = the colleague's worktree path on the unmounted share; `<scratch>` = retired worktree path; `<keep>` = a preservation directory **outside** the checkout being removed.

```sh
# 1. Inventory first — establishes registration, paths, branches, locks.
git -C "<primary-root>" worktree list --porcelain -z
```
*Check:* `<completed>` must appear with its branch `task/completed` and HEAD. If — and only if — `<completed>` shows as displaced/missing rather than registered, repair before anything else and re-list:
```sh
git -C "<primary-root>" worktree repair "<completed>"
git -C "<primary-root>" worktree list --porcelain -z
```
Do **not** repair `<offline>`: its share is unmounted, not relocated.

```sh
# 2. Protect the in-use offline checkout before any prune is even considered.
#    (Lock state is printed as a `locked` line in step 1.)
git -C "<primary-root>" worktree lock \
  --reason "offline worker on unmounted share; in use by colleague" "<offline>"
```
*Check:* re-list and confirm `locked` is now present for `<offline>`. Skip locking only if already locked — read the existing reason; never unlock it.

```sh
# 3. Establish the completed checkout's state.
git -C "<completed>" status --short --branch --untracked-files=all
git -C "<completed>" status --short --ignored
git -C "<completed>" rev-parse HEAD
git -C "<primary-root>" rev-parse refs/heads/task/completed
git -C "<completed>" submodule status
```
*Check:* HEAD must equal the branch tip; the `--ignored` listing should show `review.db` as the only item of value; no in-progress operation (e.g. `<completed>/.git` merge/rebase state), no other uncommitted or untracked work.

```sh
# 4. Verify the squash integration (ancestry is broken by squashing).
git -C "<primary-root>" merge-base --is-ancestor refs/heads/task/completed release
# ^ Expected non-zero: squash breaks ancestry, so prove content instead:
git -C "<primary-root>" log --oneline --decorate -n 10 release        # identify the squash commit
git -C "<primary-root>" diff --stat "<squash-commit>^" "<squash-commit>"
git -C "<primary-root>" diff --stat "<base-commit>"  refs/heads/task/completed
git -C "<primary-root>" diff --quiet "refs/heads/task/completed^{tree}" "<squash-commit>^{tree}"
```
*Check:* diffs equivalent / tree comparison exit 0 (or differences reviewed and explained by later `release` commits). Record the squash commit SHA for the report. A closed/merged state alone is not evidence.

```sh
# 5. Preserve what the reviewer needs, outside the deletion path.
mkdir -p "<keep>"
cp -p "<completed>/review.db" "<keep>/review.db"
sha256sum "<completed>/review.db" "<keep>/review.db"
```
*Check:* both checksums identical **before** step 6. A clean `git status` never proves ignored files survive removal.

```sh
# 6. Reclaim the checkout (branch is deliberately untouched).
git -C "<primary-root>" worktree remove "<completed>"
```
*Check:* if Git refuses, do **not** reach for `--force` — re-read the refusal, resolve the cause (re-verify preservation), and only proceed with `--force` on explicit authorization. Verify absence:
```sh
git -C "<primary-root>" worktree list --porcelain -z     # <completed> gone
git -C "<primary-root>" show-ref --verify --quiet refs/heads/task/completed
```
**No `branch -d`:** the review on `task/completed` is still open; squash already broke `-d`'s ancestry check anyway.

```sh
# 7. Prune only the retired scratch registration — dry run first.
git -C "<primary-root>" worktree prune --dry-run --verbose
```
*Check:* every listed entry must be exactly `<scratch>` (directory already deleted intentionally). **Stop** if `<offline>` or `<completed>` appears. Only then:
```sh
git -C "<primary-root>" worktree prune --verbose
```

```sh
# 8. Final verification.
git -C "<primary-root>" worktree list --porcelain -z
sha256sum "<keep>/review.db"
git -C "<primary-root>" show-ref refs/heads/task/completed
```

## What remains

- **Branch `task/completed`** — retained at its recorded tip; the review is open. Its changes are **not** an ancestor of `release` (squash), verified content-wise against squash commit `<squash-commit>`, which is reported as the integration commit.
- **`<keep>/review.db`** — the ignored review database, preserved outside the removed path, checksum-verified.
- **`<offline>`** — colleague's checkout, **retained and locked** with an explicit reason; not pruned, not unlocked, not repaired (share unmounted, still in use).
- **Removed:** only `<completed>` (registration + directory, via `worktree remove`) and the stale registration for `<scratch>` (via reviewed `prune`). No directory was ever deleted by filesystem commands; no branch, ref, or shared objects were purged.
