No repo in `/tmp/skill-up-1277081675` — only `.opencode/` — so no base/target can be inferred here.

Do not assume `main` is the integration target:

* `Base` = commit/ref you start from. `Integration target` = branch intended to receive the work. They may differ.
* Use requested base if given, otherwise inspect repo conventions (`CONTRIBUTING`, PR template, default branch, recent merges). If current remote base required, fetch then resolve ref before creation.

For feature X:

* Implementation: task worktree + task branch, reused for continuation:
  `git -C "<repo>" worktree add -b "<task-branch>" "<worktree>" "<base-ref>"`
* Disposable inspection/testing only: detached HEAD, no branch:
  `git -C "<repo>" worktree add --detach "<worktree>" "<commit>"`
  Anchor valuable detached commits to a branch before removal.

Never override checkout protection — if `<task-branch>` is checked out elsewhere, reuse that checkout via owner or use a different branch. Don't use `-B` unless resetting that branch is authorized.

To proceed I need:
1. Repo path (`<repo>`) containing feature X
2. Requested base ref/commit, if any
3. Intended integration target branch/PR workflow
4. Desired task branch name + worktree location convention, or disposable path for inspection
