Do not assume `main` is the integration target.

* `Base` vs `target` differ: base is commit/ref you start from, target is branch to receive it. Inspect repo conventions — `CONTRIBUTING`, PR template, default branch — and resolve current remote ref with fetch before creation. No repo in `/tmp/skill-up-4267842627` to verify against.
* Feature X development: task worktree + task branch, not current checkout if concurrent/conflicting work needed:
  `git -C "<repo>" worktree add -b "<task-branch>" "<worktree>" "<base-ref>"`
  Reuse that branch for continuation; if checked out elsewhere, reuse that checkout or use a different branch. Never override checkout protection. Don't use `-B` unless reset is authorized.
* Disposable inspection/testing only: detached HEAD:
  `git -C "<repo>" worktree add --detach "<worktree>" "<commit>"`
  Anchor valuable commits to a branch before removal.

Keep explicit: checkout absolute path, branch / detached commit, starting commit, integration target, manager.
