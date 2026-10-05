## Plan and exact command sequence (no repo present here — run these in order)

Placeholders: `<repo>` = main checkout/bare root holding worktree metadata; `<completed>` = `case02/checkouts/completed`; `<worker>` = offline-worker checkout path; `<scratch>` = retired scratch path; `<archive>` = durable dir *outside* `<completed>` for review files.

### 1. Establish the inventory (no mutations)

```sh
git -C "<repo>" worktree list --porcelain -z
git -C "<repo>" status --short --branch
```

Record each path, HEAD, branch, and any `locked`/`prunable`/`detached` lines. Confirm `<completed>` is on `task/completed`, `<worker>` is the entry for the unmounted share, and `<scratch>` still has a registration.

### 2. Inspect the completed checkout before touching it

```sh
git -C "<completed>" status --short --branch --untracked-files=all
git -C "<completed>" status --short --ignored
git -C "<completed>" rev-parse HEAD
git -C "<completed>" branch --show-current
git -C "<completed>" ls-files -o -i --exclude-standard
```

Expect: clean tracked state, branch `task/completed`, and ignored `review.db` as the only artifact of interest.

### 3. Preserve what the review needs, out of the deletion path

```sh
mkdir -p "<archive>"
mv "<completed>/review.db" "<archive>/review.db"
sha256sum "<archive>/review.db"
git -C "<completed>" status --short --ignored
```

The last command should now show no ignored files left. Any other needed state (detached commits, untracked scripts, ongoing operations) must be anchored/copied before proceeding — if anything unexpected appears, stop.

### 4. Verify integration into `release` before removal

```sh
git -C "<repo>" log --oneline -5 release
git -C "<repo>" show --stat release | head -50
git -C "<repo>" merge-base --is-ancestor "$(git -C "<completed>" rev-parse HEAD)" release
```

Squash integration typically breaks ancestry, so treat the failed `is-ancestor` check as expected; confirm the squashed `release` commit carries the `task/completed` changes by comparing the diff of `task/completed`'s tip against `release`:

```sh
git -C "<repo>" diff "$(git -C "<completed>" rev-parse HEAD)"..release --stat
```

### 5. Remove the completed checkout (keep its branch — review is open)

```sh
git -C "<repo>" worktree remove "<completed>"
git -C "<repo>" worktree list --porcelain -z
```

Require exit 0 and omit `--force`; if Git refuses, stop and report the dirty/untracked cause rather than forcing. Do **not** run `branch -d task/completed` — the open review still needs it.

### 6. Protect the offline-worker registration (do not clean it)

Check its entry from step 1 for a `locked` line.

```sh
# Only if it is currently unlocked:
git -C "<repo>" worktree lock --reason "colleague-owned offline-worker checkout; share unmounted; still in use" "<worker>"
```

Do not remove, unlock, prune, or move `<worker>`.

### 7. Prune only the retired scratch registration

```sh
git -C "<repo>" worktree prune --dry-run --verbose
git -C "<repo>" worktree prune --verbose
```

Review the dry-run output first: **every** listed entry must be the intentionally deleted scratch checkout. The locked worker must not appear. Do not pass custom `--expire` values.

### 8. Final verification

```sh
git -C "<repo>" worktree list
git -C "<repo>" branch --list task/completed release
ls -l "<archive>/review.db"
```

## What remains (report exactly this)

- **Branch `task/completed`**: retained — review still open; work is squash-integrated into `release` but the branch ref preserves the pre-squash history for the reviewer.
- **`<archive>/review.db`**: preserved (moved, not copied-then-lost), outside any removed path.
- **Offline-worker checkout `<worker>`**: registration retained, locked with a reason, path currently unavailable; colleague-owned and still in use — untouched.
- **`release`**: holds the squash-integrated integration commit.

Removed/pruned: the `<completed>` checkout registration (directory gone, `review.db` evacuated first), and the stale registration for the retired, already-deleted `<scratch>` checkout (pruned after reviewed dry run).
