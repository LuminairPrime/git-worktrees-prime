Do not assume `main` is the integration target.

* **Base vs target:** `base` = commit/ref you start from, `integration target` = branch intended to receive it. They may differ. Use requested base; otherwise inspect repo conventions for normal target - don't assume `main`/`master`/`origin`/`HEAD`.
* **Feature X work:** create task branch for development:
  `git -C "<repo>" worktree add -b "<task-branch>" "<worktree>" "<base-ref>"`
  Reuse it for continuation. If that branch is checked out elsewhere, reuse that checkout via owner or use a different branch. Never override checkout protection. Don't use `-B` unless branch reset is authorized.
* **Disposable inspection:** use detached HEAD only:
  `git -C "<repo>" worktree add --detach "<worktree>" "<commit>"`
  Anchor any valuable detached commit to a branch before removal.

To proceed I need: repo path, desired `base-ref`, `integration target`, and `task-branch` + `worktree` path.
