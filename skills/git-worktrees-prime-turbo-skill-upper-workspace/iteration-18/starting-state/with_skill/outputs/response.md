Do not assume `main` is the integration target:

* `Base` (where you start) vs `integration target` (where it merges) may differ. Use the requested base; otherwise inspect the repo's normal target — do not assume `main`/`master`/`origin`/`HEAD`.
* If a current remote base is required, fetch then resolve it before creation. Record path, branch, starting commit, target, and manager.

For feature X:

* Development: task worktree with task branch: `git -C "<repo>" worktree add -b "<task-branch>" "<worktree>" "<base-ref>"`
* Reuse that branch/checkout for continuation. If the branch is checked out elsewhere, reuse via owner or create a different branch — never override checkout protection. Don't use `-B` unless branch reset is authorized.
* Disposable inspection/testing only: detached HEAD: `git -C "<repo>" worktree add --detach "<worktree>" "<commit>"`. Anchor any valuable detached commits to a branch before removal.

