## Short answer: No — do not run `git worktree move` on either one

`git worktree move` is only valid for **linked** worktrees, and it **refuses** to move a worktree that contains submodules (it also cannot move the main worktree). So both of your planned moves are the two cases that fail. Here is exactly what I would run, in order.

---

### Step 0 — Inventory (before any change)

Run from the main checkout or the bare repository:

```sh
git -C "<repo>" worktree list --porcelain -z
```

Parse the output to confirm, for each entry: absolute path, `bare`, `HEAD`, `branch`, and `locked`/`prunable` flags. Identify which entry is the **main** worktree (the primary root) and which is the **linked task checkout**.

### Step 1 — Identify the two blockers

```sh
# 1. Is this the main worktree?
git -C "<repo>" rev-parse --git-common-dir
git -C "<worktree>" rev-parse --git-dir
# If the worktree's git-dir == git-common-dir, it's main → move is not permitted.

# 2. Does this checkout contain submodules?
git -C "<worktree>" submodule status
# or: test -f "$(git -C "<worktree>" rev-parse --show-toplevel)/.gitmodules" && echo HAS_SUBMODULES
```

Result:

- **Main checkout** → `git worktree move` will refuse it. Do not attempt.
- **Linked checkout with submodules** → `git worktree move` will refuse it (`fatal: ... submodule`-type refusal). Do not attempt either.

### Step 2 — What to do for the main checkout (manual relocate + repair)

There is no `git worktree move` for main. The supported path is: move the directory yourself **preserving `.git` intact**, then reconnect:

```sh
# Optional but recommended: stop anything holding the directory open.
# Then, from outside both trees:
mv "<primary-root>" "<new-primary-root>"

# Repair FIRST — before cd, status, checkout, or any pruning decision:
git -C "<new-primary-root>" worktree repair "<new-primary-root>"

# Repair every linked worktree too: their registrations point at old paths,
# and the main worktree's path is recorded in each linked worktree's .git file.
git -C "<new-primary-root>" worktree repair "<path-to-linked-worktree>" ...
# (If a linked worktree also moved: run repair with its NEW absolute path.)

# Verify
git -C "<new-primary-root>" worktree list --porcelain -z
```

> Note: if only the *main* directory moved, running `git worktree repair` from the new main location with the linked worktrees' paths re-records everything; if a linked worktree moved, pass its new path as shown above.

### Step 3 — What to do for the linked checkout with submodules

`worktree move` is off the table, so use the same relocate-and-repair pattern (this is the sanctioned fallback):

```sh
mv "<linked-worktree>" "<new-linked-path>"

# Reconnect the registration from the main checkout / bare repo:
git -C "<primary-root>" worktree repair "<new-linked-path>"

# Rebuild submodule checkouts at the new location (registrations live under
# each submodule's .git file and point at the old absolute path):
git -C "<new-linked-path>" submodule update --init --recursive
# If submodule state looks stale, repair submodule registrations too:
git -C "<new-linked-path>" submodule foreach --recursive 'git submodule repair "$toplevel/$name"'

# Verify
git -C "<new-linked-path>" rev-parse --show-toplevel
git -C "<new-linked-path>" status --short --branch
git -C "<new-linked-path>" submodule status
git -C "<primary-root>" worktree list --porcelain -z
```

Preserve `.git` and all contents during the `mv` — never recreate the checkout or delete/rewrite worktree metadata by hand.

### Step 4 — Only if a directory was already moved outside Git

If any of these moves has *already* happened via file manager/`mv`, the skill rule applies: the very first command is repair, with the checkout's **current** absolute path — not `cd`, `status`, or pruning:

```sh
git -C "<repo-or-new-primary>" worktree repair "<current-absolute-path>"
git -C "<repo-or-new-primary>" worktree list --porcelain -z   # re-verify inventory
```

### What I would explicitly **not** run

- `git worktree move "<primary-root>" ...` — invalid for main.
- `git worktree move "<linked-with-submodules>" ...` — invalid with submodules.
- `git worktree prune` — never as part of a relocation; it only drops stale *metadata*, and could delete registrations for an offline volume.
- Any `rm -rf` / recreate of a live checkout to "fix" a path.

**Bottom line:** run the inventory and the two identification checks first; both planned `git worktree move` invocations should be skipped, and each checkout relocated with `mv` + `git worktree repair` (plus `submodule update` for the linked one), then re-verify with `worktree list --porcelain -z`.
