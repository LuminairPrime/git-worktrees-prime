Do not assume `main` is the integration target.

* **Base:** use the requested base. If none, inspect repo conventions (CONTRIBUTING, open PRs, default branch) to find the normal target — do not default to `main`/`master`/`origin`/current `HEAD`.
* If a current remote base is required: fetch that remote first, then resolve `<base-ref>^{commit}` before creation. Do not `pull` into someone else's checkout.
* Record: checkout path, branch, starting commit, integration target, manager.

**Task branch vs disposable checkout:**

* Feature X implementation: create a task branch in a new worktree:
  `git -C "<repo>" worktree add -b "<task-branch>" "<worktree>" "<base-ref>"`
  Reuse the branch on continuation. If already checked out elsewhere, reuse that checkout or use a different branch — never override checkout protection, never use `-B` without reset authorization.
* Disposable inspection/testing only: use detached HEAD:
  `git -C "<repo>" worktree add --detach "<worktree>" "<commit>"`
  Anchor any valuable detached commit to a branch before removal.

