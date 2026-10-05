Before offline — lock it, do not prune it while unavailable:

1. Confirm canonical registration:
   `git -C "<repo>" worktree list --porcelain -z`
   Verify exact absolute `<worktree>` path and branch.

2. Lock before unmount:
   `git -C "<repo>" worktree lock --reason "share offline <date> - task still active" "<worktree>"`
   This blocks `git gc` / `gc.worktreePruneExpire` from auto-dropping the missing registration.

3. Verify lock held:
   `git -C "<repo>" worktree list --porcelain -z`

While unavailable — do not prune:

* Do NOT run `git worktree prune`, `git worktree prune --expire ...`, or `git gc`.
* Do NOT `unlock` it just because the path is missing.
* Missing directory = possibly offline volume, not stale metadata. Prune only if every dry-run entry is an intentionally removed worktree.

