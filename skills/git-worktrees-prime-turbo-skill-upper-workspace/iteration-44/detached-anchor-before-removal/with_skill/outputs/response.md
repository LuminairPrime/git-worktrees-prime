**No — you can't just remove it.** Commits made on a detached `HEAD` have no branch pointing at them. Their only live reference is that worktree's own `HEAD` (via its reflog). `git worktree remove` destroys that reference, so your three commits become unreachable and are eventually dropped by `gc` (only `ORIG_HEAD`-style reflog luck would keep them, briefly). The skill's rule is explicit: *anchor valuable detached commits to a branch before removal.*

Here are the exact checks and commands, in order. Placeholders: `<worktree>` = the disposable checkout's absolute path, `<repo>` = a surviving checkout (main worktree or a bare repo), `<task-branch>` = a name you choose, `<integration-ref>` = the branch you'd merge into.

### 1. Inventory — confirm the detached state and see everything at risk

```sh
git -C "<repo>" worktree list --porcelain -z
git -C "<worktree>" status --short --branch --untracked-files=all
git -C "<worktree>" status --short --ignored
git -C "<worktree>" rev-parse HEAD
```

The status line should show `HEAD detached at ...`. Also record the commit before the base (the start of your three commits):

```sh
git -C "<worktree>" log --oneline -4 HEAD
```

Anything dirty or untracked in step 1 must be committed, stashed, or explicitly authorized to discard before removal — a clean status does **not** cover ignored files or detached commits.

### 2. Preserve the detached commits — create the branch at `HEAD` *before* removing anything

```sh
git -C "<worktree>" branch "<task-branch>" HEAD
git -C "<repo>" show-ref --verify --quiet "refs/heads/<task-branch>"
git -C "<worktree>" log --oneline -4 "<task-branch>"
```

Run the branch creation **from the disposable worktree** (the ref lives in the shared repo, so location barely matters, but `HEAD` resolves unambiguously there). Exit 0 from `show-ref` and a log whose tip matches your `rev-parse HEAD` from step 1 prove the three commits are now anchored to a durable ref. Only now is the checkout removable.

### 3. Verify it's safe to remove this exact checkout

```sh
git -C "<repo>" worktree list --porcelain -z
```

Confirm `<worktree>`'s canonical absolute path, that it is a **linked** worktree (not the primary/main checkout), not your current working directory, not its parent, and not a sibling task. Also confirm no agent/editor/terminal/service is still using it.

### 4. Remove the checkout (branch survives)

```sh
git -C "<repo>" worktree remove "<worktree>"
```

If it refuses because of uncommitted changes, go back to step 1 and resolve them — don't reach for `--force` without explicit authorization for the data loss.

### 5. Verify

```sh
git -C "<repo>" worktree list --porcelain -z
git -C "<repo>" log --oneline -4 "<task-branch>"
```

The removed path must be gone from the list, and the branch log must still show all three commits.

### 6. Only if stale metadata remains (optional)

```sh
git -C "<repo>" worktree prune --dry-run --verbose
# Review every entry; prune only if all are intentionally removed worktrees.
git -C "<repo>" worktree prune --verbose
```

### 7. Branch deletion — a separate decision, later

Do **not** delete `<task-branch>` now; it's the only thing holding your commits. Delete it only after its work is verified integrated:

```sh
git -C "<repo>" merge-base --is-ancestor "<task-branch>" "<integration-ref>"
```

Exit 0 proves ancestry; only then `git -C "<repo>" branch -d "<task-branch>"`. If that check fails or `branch -d` refuses, keep the branch — `branch -D` requires explicit authorization after verifying the history.

**Bottom line:** the *only* thing that must happen first is step 2 — anchor the three commits to a branch (`git -C "<worktree>" branch "<task-branch>" HEAD`) and verify it with `show-ref`/`log`. After that, `git worktree remove` is safe.
