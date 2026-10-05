Following the skill's cleanup decision tree, here is the exact sequence, run from the primary (main) checkout — never from inside `case02/checkouts/completed`. `<primary-root>` is the main worktree path; all paths should be the canonical absolute paths from the porcelain inventory.

## Phase 0 — Inventory and identity checks

```sh
git -C "<primary-root>" worktree list --porcelain -z
```

Confirm from the output, before touching anything:
- The `completed` checkout's canonical absolute path and that its `HEAD` is `refs/heads/task/completed`.
- The `offline-worker` entry (colleague's, share unmounted) and the retired `scratch` entry (directory already gone).
- That `case02/checkouts/completed` is **not** the primary worktree, not your current working directory, and not a parent of it. Ensure no task-owned terminal/service/editor is still holding it.

## Phase 1 — Verify integration status (informs, but does not authorize branch deletion)

```sh
git -C "<primary-root>" rev-parse --verify "release^{commit}"
git -C case02/checkouts/completed rev-parse HEAD
git -C "<primary-root>" merge-base --is-ancestor task/completed release
```

Expected: the ancestry check exits **1** — squash integration broke ancestry, so the old task tip is not an ancestor of `release`. That is expected, not an error. Verify the replacement instead:

```sh
# The recorded squash/integration commit must be on release (expect exit 0):
git -C "<primary-root>" merge-base --is-ancestor "<squash-commit>" "release"
git -C "<primary-root>" diff --stat task/completed release
```

Regardless of outcome here: **the branch is retained** because the review on `task/completed` is still open. No `git branch -d` (it would refuse anyway), and absolutely no `git branch -D`.

## Phase 2 — Inspect the checkout's local state

```sh
git -C case02/checkouts/completed rev-parse --show-toplevel
git -C case02/checkouts/completed status --short --branch --untracked-files=all
git -C case02/checkouts/completed status --short --ignored
```

Require, before removal: tracked state clean, no merge/rebase/cherry-pick in progress, `HEAD` attached at the `task/completed` tip (no stranded detached commits). Expect `review.db` to appear only in the `--ignored` output as `!! review.db`. Other ignored entries (build outputs) are reproducible and need no backup.

## Phase 3 — Preserve `review.db` outside the deletion path

```sh
mkdir -p "<primary-root>/review-artifacts"
cp -p case02/checkouts/completed/review.db "<primary-root>/review-artifacts/task-completed.review.db"
sha256sum case02/checkouts/completed/review.db "<primary-root>/review-artifacts/task-completed.review.db"
```

Require matching hashes before proceeding. Hand the preserved path to the reviewer.

## Phase 4 — Remove the completed checkout

```sh
git -C "<primary-root>" worktree remove "/abs/path/case02/checkouts/completed"
```

This should succeed without `--force` (clean status; the ignored `review.db` doesn't block removal and is already preserved). Do not delete the directory via filesystem tools, and do not use `--force` to silence an unexpected refusal — investigate instead.

## Phase 5 — Prune stale registrations, protecting the offline checkout

```sh
git -C "<primary-root>" worktree prune --dry-run --verbose
```

Expected dry-run entries: `scratch` **and** `offline-worker`. The rule is: prune only if *every* dry-run entry is an intentionally removed worktree — a missing directory may be an offline volume, so do **not** prune yet.

```sh
git -C "<primary-root>" worktree lock --reason "colleague-owned checkout on unmounted share, still in use — do not prune" "/abs/path/offline-worker"
```

Locking is protective metadata only; it touches nothing of the colleague's files and exempts the registration from pruning. Re-run the dry run with **identical options**:

```sh
git -C "<primary-root>" worktree prune --dry-run --verbose
```

Now the only entry must be the retired `scratch` checkout — an intentionally removed worktree. Only then:

```sh
git -C "<primary-root>" worktree prune --verbose
```

(If locking a colleague's registration were considered beyond your authority, the safe alternative is to skip pruning entirely and report the scratch registration as retained stale metadata — never prune while the offline-worker appears in the dry run.)

## Phase 6 — Verify the result

```sh
git -C "<primary-root>" worktree list --porcelain -z
git -C "<primary-root>" show-ref --verify refs/heads/task/completed
ls -l "<primary-root>/review-artifacts/task-completed.review.db"
```

## What remains, precisely

- **Branch `refs/heads/task/completed`** — retained deliberately; the review is still open, and squash integration means it is not an ancestor of `release` (so `-d` would refuse). Its work is also preserved in the squash commit on `release`.
- **`review.db`** — preserved at `<primary-root>/review-artifacts/task-completed.review.db` (hash-verified copy) for the reviewer; the original is gone with the checkout.
- **Checkout `case02/checkouts/completed`** — removed (directory and registration); nothing else of value was in it.
- **`offline-worker` checkout** — registration retained, now **locked** with the recorded reason; directory untouched, not pruned, not unlocked. Read the lock reason before any future unlock, and re-verify with the colleague once the share is back.
- **Retired `scratch` checkout** — stale registration pruned (directory was already intentionally deleted); no branch or object data touched.
- **Primary checkout, shared objects, reflogs, and all other refs** — untouched.
