# Moving the Main Checkout and a Linked Worktree with Submodules

Yes, proceed — but in a specific order, and with submodule pointer repair afterward. Here is the exact sequence.

---

## Phase 1 — Pre-flight checks (run in order)

### 1. Inventory all worktrees and check for locks

```bash
git worktree list --porcelain
```

**Check for:**
- Any line containing `locked` — a locked worktree **cannot** be moved. Unlock with `git worktree unlock <path>` first.
- Any line containing `prunable` — a worktree whose directory is missing. Run `git worktree prune` to clean up before moving.
- Confirm which path is the **main** checkout (the one with a `.git` *directory*, not a file).

### 2. Ensure the main checkout is clean

```bash
cd /path/to/main/checkout
git status
```

**Must be clean:** no staged/unstaged changes, no untracked files you care about, and no in-progress operation (merge, rebase, cherry-pick, bisect, am). If any of these are present, resolve or stash them first.

### 3. Ensure the linked worktree is clean

```bash
cd /path/to/linked/worktree
git status
```

Same requirements as above.

### 4. Check submodule state in the linked worktree

```bash
git submodule status --recursive
```

**Every submodule must be clean** (no `+` prefix meaning different commit checked out, no `-` prefix meaning uninitialized). If any submodule has local modifications, commit or stash them inside the submodule first. `git submodule update` after the move will reset dirty submodules.

### 5. Verify destination paths are safe

```bash
ls -la /new/main/path
ls -la /new/linked/path
```

Each destination must **not exist** or be an **empty directory**. `git worktree move` refuses to overwrite a non-empty directory.

### 6. Confirm no processes are using either worktree

Close any editors, IDEs, terminals, servers, or build tools that have these directories open.

---

## Phase 2 — The moves (in this order)

### 7. Move the main checkout first

```bash
cd /path/to/main/checkout
git worktree move /new/main/path
```

**Why first:** This moves the `.git` directory and automatically updates the `gitdir:` pointer in **every** linked worktree's `.git` file to point to the new main location. Doing this first means the linked worktree's superproject pointer is already correct when you move it.

**What it does NOT do:** It does **not** update submodule `.git` files inside linked worktrees. Those still point to the old `/old/main/path/.git/modules/...` and are now broken.

### 8. Move the linked worktree

```bash
git worktree move /path/to/linked/worktree /new/linked/path
```

This moves the working directory. The `.git` file inside it (already updated in step 7) continues to point to the correct location in the main repo's `.git/worktrees/` directory.

### 9. Repair submodule pointers in the linked worktree

```bash
cd /new/linked/path
git submodule update --init --recursive
```

This rewrites each submodule's `.git` file to point to `/new/main/path/.git/modules/<submodule>` and checks out the correct commits.

> **If the main checkout also has submodules**, run the same command there:
> ```bash
> cd /new/main/path
> git submodule update --init --recursive
> ```

---

## Phase 3 — Post-move verification

### 10. Verify worktree list and pointers

```bash
cd /new/main/path
git worktree list
```

All paths should show the new locations with no errors.

### 11. Verify main checkout health

```bash
git status
git submodule status --recursive   # if applicable
```

### 12. Verify linked worktree health

```bash
cd /new/linked/path
git status
git submodule status --recursive
```

### 13. Safety net — repair any remaining pointer issues

If anything still looks broken (e.g., a worktree was locked and you forced things, or a submodule pointer is still wrong):

```bash
git worktree repair
```

This scans all worktrees and fixes stale `gitdir` pointers.

---

## Summary of the critical gotchas

| Gotcha | Mitigation |
|---|---|
| Submodule `.git` files break when the main repo moves | Run `git submodule update --init --recursive` after the move |
| Locked worktrees refuse to move | `git worktree unlock` first |
| Dirty submodules get reset by the repair | Ensure submodules are clean before moving |
| Moving the main checkout breaks all linked worktrees if done with plain `mv` | Use `git worktree move`, which updates pointers automatically |
| Destination must not exist or be empty | Verify with `ls` before moving |
