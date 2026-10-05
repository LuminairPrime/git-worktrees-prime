## Assumptions for the placeholders

- `<repo>` = the main worktree (or bare repo) that registers all three checkouts — you never `cd` first; every command names `-C <repo>` or an explicit checkout path.
- `WT` = absolute path of `case02/checkouts/completed`.
- No move/rename of `WT` was reported, but registration is checked before anything else anyway.

---

## Phase 0 — Inventory first (read-only, no `cd`, no `status`)

```sh
# 1. Full registration inventory, machine-parseable (-z; split on NUL).
git -C <repo> worktree list --porcelain -z | tr '\0' '\n'

# 1b. ONLY if the inventory shows WT's recorded path missing/mismatched
#     with case02/checkouts/completed -> repair BEFORE cd/status/checkout:
git -C <repo> worktree repair "$WT"
git -C <repo> worktree list --porcelain -z | tr '\0' '\n'
```

**Check:** you can now name, for each entry, its `worktree` path, `HEAD`, `branch`, plus any `locked`/`prunable` lines. Expect four logical entries: `<repo>` (main), `completed`, the offline-worker path, and the retired-scratch entry (likely reported `prunable`). Stop and re-read the inventory if anything else appears.

---

## Phase 1 — Establish `WT`'s state and ownership

```sh
# 2. Confirm identity of the exact directory before touching it.
git -C "$WT" rev-parse --show-toplevel
git -C "$WT" branch --show-current
git -C "$WT" rev-parse HEAD            # record this SHA as <task-tip>

# 3. Dirty / untracked / ignored inventory — ignored files are the payload here.
git -C "$WT" status --short --branch --untracked-files=all
git -C "$WT" status --short --ignored
git -C "$WT" check-ignore -v review.db # exit 0 = confirmed ignored

# 4. No unfinished Git operation and no other consumer.
test -e "$(git -C "$WT" rev-parse --git-path index.lock)" && echo "BUSY: index.lock" # must print nothing
```

**Checks:** `branch --show-current` = `task/completed`; `review.db` is present and is (expected) the only ignored item; no `index.lock`; `WT` is not `<repo>` itself, not the cwd, not a parent of `<repo>`.

---

## Phase 2 — Verify squash integration (ancestry will NOT hold)

```sh
# 5. Resolve the integration target explicitly; do not assume its name is right.
git -C <repo> rev-parse --verify refs/heads/release^{commit}

# 6. The squash broke ancestry — expect NON-zero here; that is expected.
git -C <repo> merge-base --is-ancestor refs/heads/task/completed refs/heads/release

# 7. Tree-equivalence instead: empty diff proves the task content is on release.
git -C <repo> diff --stat <task-tip> refs/heads/release   # expect: empty output, exit 0

# 8. Show the squash commit for the record.
git -C <repo> log --oneline -3 refs/heads/release
```

**Checks:** step 7 empty ⇒ every change in `WT`'s tip is present on `release`. Step 6 failing is precisely why the branch may **not** be deleted with `-d`, and why `-D` is out of scope (open review).

---

## Phase 3 — Preserve `review.db` outside the removal path

```sh
# 9. Destination must be OUTSIDE every worktree (not inside <repo>).
PRESERVED="$(realpath -m case02/review-artifacts/completed)"
mkdir -p "$PRESERVED"

# 10. Copy, keeping metadata, then prove byte-identity BEFORE deletion.
cp -p "$WT/review.db" "$PRESERVED/review.db"
cmp "$WT/review.db" "$PRESERVED/review.db"      # exit 0
sha256sum "$WT/review.db" "$PRESERVED/review.db" # identical digests
ls -l "$PRESERVED/review.db"
```

**Check:** `cmp` exit 0 and equal hashes. Do not proceed to Phase 4 until this passes — `git worktree remove` deletes ignored files along with the directory.

---

## Phase 4 — Reclaim the `completed` checkout

```sh
# 11. Re-verify the exact target immediately before removal (path, branch, HEAD, registration).
git -C <repo> worktree list --porcelain -z | tr '\0' '\n'
test "$(git -C "$WT" rev-parse --show-toplevel)" = "$WT"

# 12. Normal removal.
git -C <repo> worktree remove "$WT"
```

**If it refuses** ("modified or untracked files"): the refusal is caused *only* by the intentionally-preserved ignored `review.db`. Since the copy is verified in step 10, this is the moment `--force` is justified for this one path:

```sh
# 13. Conditional — only after step 10's verification, only for this exact path.
git -C <repo> worktree remove --force "$WT"
```

```sh
# 14. Confirm directory is gone.
test -e "$WT" && echo "STILL PRESENT" || echo "removed"
```

**Never** remove by `rm -rf`; only `git worktree remove`.

---

## Phase 5 — Branch `task/completed` (review still open → keep)

```sh
# 15. Prove the branch survives checkout removal.
git -C <repo> show-ref --verify --quiet refs/heads/task/completed   # exit 0
git -C <repo> log --oneline -1 refs/heads/task/completed
```

**Decision:** review open ⇒ **no `branch -d`, no `branch -D`.** Removing a worktree leaves its branch; the review continues from this ref. (Steps 6–7 already showed `-d` would refuse anyway.)

---

## Phase 6 — Offline-worker checkout (colleague-owned, unmounted share)

```sh
# 16. Identify it and read its state — it will likely show as prunable.
git -C <repo> worktree list --porcelain -z | tr '\0' '\n'
```

```sh
# 17. Protect it before any prune: lock with an explicit reason (reason BEFORE path).
git -C <repo> worktree lock --reason "offline worker checkout on unmounted share; owned by colleague, still in use" "<offline-worktree-abs-path>"
git -C <repo> worktree list --porcelain -z | tr '\0' '\n'   # must now show `locked`
```

**Checks / prohibitions:** a missing directory here means *unmounted*, not deleted. **Do not remove it, do not unlock it, do not prune it, do not touch its branch.** If the lock command fails because the path cannot be resolved, **stop Phase 7 entirely** and defer pruning until the share is remounted.

---

## Phase 7 — Retired scratch checkout (already deleted from disk)

```sh
# 18. Dry run FIRST; review every single line.
git -C <repo> worktree prune --dry-run --verbose
```

**Gate:** the output must contain **only** the retired scratch path. Because the offline worktree is now locked it must be absent from this list. If any other path appears (live checkout, `<repo>` itself, the offline share) → **do not run step 19.**

```sh
# 19. Prune registrations only (never branches, never directories).
git -C <repo> worktree prune --verbose
```

```sh
# 20. Report-only: any leftover scratch branch is out of scope for deletion.
git -C <repo> branch --list
```

---

## Phase 8 — Final verification

```sh
git -C <repo> worktree list --porcelain -z | tr '\0' '\n'
git -C <repo> show-ref --verify --quiet refs/heads/task/completed && \
  git -C <repo> log --oneline -1 refs/heads/task/completed
test -e "$WT" && echo "completed checkout still present" || echo "completed checkout gone"
cmp "$WT_OLD/review.db" "$PRESERVED/review.db" 2>/dev/null || sha256sum "$PRESERVED/review.db"
```

**Expected final inventory:** `<repo>` (main) + the offline-worker checkout with a `locked` reason. No `prunable` entries except none; `case02/checkouts/completed` absent.

---

## Precisely what remains

| Item | State |
|---|---|
| **Checkout `case02/checkouts/completed`** | **Reclaimed** — directory removed, registration removed. |
| **`review.db`** | **Preserved** at `case02/review-artifacts/completed/review.db`, byte-identical (`cmp` exit 0, matching SHA-256) — reviewer's copy lives outside the deleted checkout. |
| **Branch `task/completed`** | **Retained** (review open). Tip `<task-tip>` verified as tree-equivalent to `release`; not deleted because squash broke ancestry and review is pending. |
| **`release`** | Holds the squash-integrated content (`git diff <task-tip> release` empty). |
| **Offline-worker checkout** | **Fully retained and untouched**: directory on the unmounted share not accessed, registration preserved and **locked with reason**; not pruned, not unlocked, branch intact; colleague's work unaffected. |
| **Retired scratch checkout** | Directory was already gone; **only its stale registration is pruned** (after a reviewed dry run). Its branch, if any, **still exists** — left alone as out of scope. |
| **Forces used** | At most `worktree remove --force` on `WT` alone, and only after `review.db` was verified preserved; nothing forced elsewhere. |
