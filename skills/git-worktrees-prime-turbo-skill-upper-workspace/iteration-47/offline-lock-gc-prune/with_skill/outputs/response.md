**Short answer:** No — do **not** prune while the share is offline. And `git gc` will not drop the registration; only an explicit `git worktree prune` (or `git worktree remove`) does that. `git worktree prune` removes registrations for worktrees whose path is missing/inaccessible, so running it while the share is unmounted would orphan the worktree. `git gc` is safe — it packs objects, prunes loose objects, and expires reflogs, but it never touches `.git/worktrees/`.

---

### Before the share goes offline (run in order)

1. Commit and push everything in the worktree so no work is lost:
   ```bash
   git -C /path/to/worktree status
   git -C /path/to/worktree add -A
   git -C /path/to/worktree commit -m "WIP: snapshot before share goes offline"
   git -C /path/to/worktree push
   ```

2. Confirm the worktree is registered in the main repo:
   ```bash
   git -C /path/to/main/repo worktree list
   ```
   You should see `/path/to/worktree` listed.

3. Confirm the worktree's `.git` link points back into the main repo:
   ```bash
   cat /path/to/worktree/.git
   ```
   It should read `gitdir: /path/to/main/repo/.git/worktrees/<name>`.

4. (Recommended) Lock the worktree so a stray `git worktree prune` cannot remove it:
   ```bash
   git -C /path/to/main/repo worktree lock /path/to/worktree --reason "share offline until <date>"
   ```
   A locked worktree is skipped by `git worktree prune` even when its path is inaccessible.

5. (Optional) Dry-run prune while the share is still online to confirm the worktree is healthy and not flagged:
   ```bash
   git -C /path/to/main/repo worktree prune --dry-run --verbose
   ```
   It should report nothing to prune (or only other stale entries).

---

### While the share is offline — do **NOT**

- Run `git worktree prune` (it would remove the registration because the path is inaccessible).
- Run `git worktree remove` on that path.
- Worry about `git gc` — it does not prune worktree registrations.

---

### After the share comes back online

1. Verify the registration is still there:
   ```bash
   git -C /path/to/main/repo worktree list
   ```

2. If the worktree is missing from the list (e.g., someone pruned it), re-establish the link:
   ```bash
   git -C /path/to/main/repo worktree repair /path/to/worktree
   ```

3. Unlock if you locked it (optional — a locked worktree still works normally):
   ```bash
   git -C /path/to/main/repo worktree unlock /path/to/worktree
   ```
