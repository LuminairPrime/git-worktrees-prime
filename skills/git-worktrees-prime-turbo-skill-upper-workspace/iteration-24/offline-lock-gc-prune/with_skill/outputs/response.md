Before offline — lock to protect registration from `gc`:

1. Confirm registration from primary repo:
   `git -C "<repo>" worktree list --porcelain -v`
   Verify exact absolute `<worktree>` path is listed.
2. Lock it:
   `git -C "<repo>" worktree lock --reason "share offline <date> - task still active, do not prune" "<worktree>"`
3. Verify lock:
   `git -C "<repo>" worktree list --porcelain -v`
   Require `locked` + reason on that entry.
4. Check auto-expire:
   `git -C "<repo>" config --get gc.worktreePruneExpire`

While unavailable — do not prune:

`git -C "<repo>" worktree prune -n -v` — review-only, do not run prune.

Do not run `git worktree prune`, `git gc`, or `git worktree unlock` just because path is missing. Missing = offline volume, not stale. Unlock/prune only after mount returns and path is verified live.

