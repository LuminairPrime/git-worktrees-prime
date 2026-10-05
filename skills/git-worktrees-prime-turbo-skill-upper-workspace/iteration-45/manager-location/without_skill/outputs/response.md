Verified everything empirically with Git 2.43.0 in a scratch repo (cleaned up afterwards). Here's the answer.

## Where to place it

With no convention to follow, derive it from the main checkout: **a sibling of `/repo`, outside every working tree**.

```sh
git -C /repo worktree add -b checkout-api ../checkout-api
# → /checkout-api
```

Caveat: `/repo` sits at the filesystem root, so its sibling is `/checkout-api`, which needs write access to `/`. If you can't or don't want that, pick one dedicated location outside any checkout (`/worktrees/checkout-api`, `~/worktrees/checkout-api`) and use it for all future tasks — that becomes your convention. Never inside `/repo`, never inside `.git/`.

## What Git enforces vs. what you must verify yourself

**Git refuses only three things** (confirmed):

| Situation | Result |
|---|---|
| Target path already exists (with content) | `fatal: '../exists' already exists` (an *empty* dir is accepted) |
| `-b` name already exists | `fatal: a branch named 'checkout-api' already exists` |
| Branch already checked out elsewhere | `fatal: 'checkout-api' is already used by worktree at '/…'` |

**Git does *not* refuse nesting** — I confirmed it happily creates a worktree inside another working tree (same repo *or* a different repo) and even inside `.git/`. So if the target is inside another checkout, these checks are on you:

1. **Confirm it's not inside any working tree or git dir.**
   ```sh
   cd <target-parent> && git rev-parse --show-toplevel
   ```
   Must fail with `fatal: not a git repository`. If it succeeds, you're nesting inside a checkout.
2. **Path doesn't exist / is empty**, and you have write permission to the parent.
3. **Branch and worktree are free:**
   ```sh
   git -C /repo worktree list
   git -C /repo show-ref --verify --quiet refs/heads/checkout-api; echo $?
   ```
4. **If you deliberately nest it anyway, know the consequences** (verified):
   - The nested worktree belongs to `/repo` (its `.git` *file* points at `/repo/.git/worktrees/…`), even though it lives inside another checkout — commands run there operate on `/repo`.
   - The outer checkout shows it as `?? checkout-api/`.
   - Outer `git add -A` → `warning: adding embedded git repository` (stores a gitlink; contents won't be shared).
   - Outer `git clean -fd` **skips** it (silent, invisible), but outer `git clean -ffdx` **deletes it** while leaving `/repo/.git/worktrees/checkout-api` behind as a stale admin entry.

**Bottom line:** place it at `/checkout-api` (sibling, outside all trees). Only place it inside another checkout after confirming the parent isn't a git working tree, the path is empty, the branch/worktree is free, and you accept the `add -A` / `clean -ffdx` hazards above.
