Do not assume `main` is the integration target.

* Base: use your requested base. If none specified, inspect repo conventions — default branch, `CONTRIBUTING`, PR template, recent merges — to find the normal target. If you need a current remote base, fetch then resolve `<base-ref>^{commit}` before creating.
* Feature `X` implementation: create a task worktree with a task branch, not detached:
  `git -C "<repo>" worktree add -b "<task-branch>" "<worktree>" "<base-ref>"`
  Reuse the branch on continuation. If checked out elsewhere, reuse that checkout or pick a different branch. Don't use `-B` unless branch reset is authorized.
* Disposable inspection: use detached HEAD only:
  `git -C "<repo>" worktree add --detach "<worktree>" "<commit>"`
  Anchor any valuable commit to a branch before removal.

No repo found in `/tmp/skill-up-1501702930` — only `.opencode/`. Provide `<repo>` path, desired `base-ref`, `<task-branch>`, and `<worktree>` path to create it.
