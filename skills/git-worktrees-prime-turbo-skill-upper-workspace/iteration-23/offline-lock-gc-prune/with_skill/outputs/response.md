Before offline — lock it. While offline — do not prune/unlock:

1. Verify registration from primary/bare repo:
`git -C "<repo>" worktree list --porcelain`
Confirm `<worktree>` absolute path present.

2. Check auto-expire window:
`git -C "<repo>" config --get gc.worktreePruneExpire`

3. Lock before unmount:
`git -C "<repo>" worktree lock --reason "share offline next week - task still active" "<worktree>"`

4. Verify locked:
`git -C "<repo>" worktree list --porcelain`
Expect `locked <reason>` for `<worktree>`.

While unavailable, do not run:
`git -C "<repo>" worktree prune`
`git -C "<repo>" worktree prune --expire <anything>`
`git gc`
`git -C "<repo>" worktree unlock "<worktree>"`

Missing = possibly offline volume, not stale. Only unlock after share returns and you have read the lock reason and verified path.

