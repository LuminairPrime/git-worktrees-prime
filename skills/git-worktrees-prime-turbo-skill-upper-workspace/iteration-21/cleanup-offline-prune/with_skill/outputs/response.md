1. Inventory — from primary checkout, not from target:
   `git worktree list -v`
   `git worktree list --porcelain -z | tr '\0' '\n'`
   `git rev-parse --show-toplevel`
   `realpath case02/checkouts/completed`
   Confirm target path/branch: `task/completed` at `case02/checkouts/completed`, owner: this task, not `offline-worker`, not primary, not cwd.

2. Verify integration target, do not assume:
   `git fetch origin`
   `git rev-parse --verify task/completed`
   `git rev-parse --verify release`
   `git log --oneline -5 release`
   `git diff release...task/completed --stat`
   Squash breaks ancestry: `git branch -d` success is not evidence. Verified only by replacement commits/diff in `release`.

3. Inspect losable state in target:
   `git -C case02/checkouts/completed status --porcelain=v1 -uall --ignored`
   `git -C case02/checkouts/completed stash list`
   `git -C case02/checkouts/completed log --oneline -3`
   `git -C case02/checkouts/completed check-ignore -v review.db`
   `ls -lh case02/checkouts/completed/review.db`
   `sha256sum case02/checkouts/completed/review.db`
   Result: tracked clean, ignored `review.db` valuable for open review.

4. Preserve outside deletion path:
   `cp case02/checkouts/completed/review.db <preserved-path>/review.db`
   `sha256sum <preserved-path>/review.db`
   Require match before removal.

5. Leave directory, remove only exact checkout via Git:
   `cd "$(git rev-parse --show-toplevel)"`
   `git worktree remove "$(realpath case02/checkouts/completed)"`
   No `rm -rf`, no `--force` unless safeguard cause resolved and authorized. No `move`.

6. Branch decision: retain:
   Do NOT run `git branch -d/-D task/completed`.
   Review remains open on `task/completed`; squash-integrated copy in `release` does not replace it. Closed/squashed PR alone insufficient.

7. Stale registrations — dry-run only:
   `git worktree prune --dry-run -v`
   Expected: `scratch` deleted-from-disk + `offline-worker` missing-because-unmounted-share.
   Rule: prune only if every entry is intentionally removed. `offline-worker` is colleague-owned, in use, unmounted volume — do NOT prune, lock/unlock, or change expiry to exclude it.
   Therefore: no `git worktree prune` executed.

8. Verify result:
   `git worktree list -v`
   `test ! -e case02/checkouts/completed && echo removed`
   `git branch --list task/completed`
   `git rev-parse --verify task/completed`
   `ls -lh <preserved-path>/review.db`

Remains:
- Removed: checkout `case02/checkouts/completed` only.
- Retained branch `task/completed` for open review.
- Retained file: `review.db` copy at `<preserved-path>/review.db`, original deleted with checkout.
- Retained registration: `offline-worker` unmounted/colleague-owned/in-use, untouched.
- Retained stale registration: retired `scratch` deleted-from-disk, prune blocked because indivisible from `offline-worker`.
- Untouched: primary checkout, `release` squash commit, remotes/objects/reflogs.

