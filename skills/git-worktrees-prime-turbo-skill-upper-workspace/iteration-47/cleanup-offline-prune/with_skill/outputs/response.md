Here is the exact sequence of commands and checks, in order:

---

## Phase 1 — Inventory and verification

```sh
# List all worktrees (parse with -z for safety)
git -C "<repo>" worktree list --porcelain -z

# Check the completed checkout's status — tracked, untracked, and ignored files
git -C "case02/checkouts/completed" status --short --branch --untracked-files=all
git -C "case02/checkouts/completed" status --short --ignored
git -C "case02/checkouts/completed" rev-parse HEAD

# Verify the branch task/completed exists
git -C "<repo>" show-ref --verify --quiet "refs/heads/task/completed"
```

**What you're confirming:**
- The completed checkout is registered and clean (no uncommitted tracked changes).
- The ignored `review.db` is present (shown by `--ignored`).
- The branch `task/completed` exists and points to the expected commit.

---

## Phase 2 — Preserve what the review needs

```sh
# Copy the ignored review.db to a safe location outside the checkout
cp "case02/checkouts/completed/review.db" "/path/to/safe/location/review.db"

# Verify the copy
ls -la "/path/to/safe/location/review.db"
```

**Why:** The reviewer still needs `review.db`. It is ignored, so it won't be in any commit — it will be lost when the checkout is removed. Copy it to a location outside the worktree path.

---

## Phase 3 — Remove the completed checkout

```sh
# Remove the worktree (no force flag — it should be clean)
git -C "<repo>" worktree remove "case02/checkouts/completed"

# Verify the branch task/completed still exists (review is still open)
git -C "<repo>" show-ref --verify --quiet "refs/heads/task/completed"
```

**Why:** The work was squash-integrated into `release`, so the changes are preserved. The branch is retained because the review is still open — a closed PR alone would be insufficient evidence, and here the review is explicitly still open.

---

## Phase 4 — Prune stale registrations

```sh
# Dry-run prune to see what would be removed
git -C "<repo>" worktree prune --dry-run --verbose

# Prune (only the retired scratch checkout's registration)
git -C "<repo>" worktree prune --verbose
```

**Why:** The retired scratch checkout was already deleted from disk, so its registration is stale. The dry-run lets you confirm that only the scratch checkout's entry is removed — the offline-worker checkout (on the unmounted share) must NOT be pruned or unlocked.

---

## Phase 5 — Verify and report

```sh
# Re-list worktrees to confirm final state
git -C "<repo>" worktree list --porcelain -z
```

---

## What remains after this sequence

| Item | Status |
|---|---|
| `case02/checkouts/completed` | **Removed** (worktree directory gone) |
| `task/completed` branch | **Retained** (review still open) |
| `review.db` | **Preserved** at the safe location you copied it to |
| Offline-worker checkout | **Untouched** (colleague-owned, still in use, on unmounted share) |
| Retired scratch checkout | **Pruned** (stale registration removed) |

---

## What you would NOT touch

- **Offline-worker checkout:** It is on an unmounted share, colleague-owned, and still in use. Do not prune, unlock, or remove it. The `worktree prune` dry-run will show it as a missing directory — that is expected and safe to leave alone.
- **The `task/completed` branch:** The review is still open, so the branch must be retained even though the work was squash-integrated into `release`.
