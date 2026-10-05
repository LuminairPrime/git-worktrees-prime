Do not assume `main` is the integration target.

* **Base vs target are different:** base = commit/ref you start from, target = branch that should receive the work. Keep both explicit: checkout path, branch, starting commit, integration target.
* **Determine target:** inspect repo conventions — default branch, CONTRIBUTING, PR template, recent merges. If you tell me the repo path I can check `git worktree list` and target for you. Current directory is not a git repo.
* **Base:** use your requested base. If you need current remote state: `fetch` the remote then `rev-parse --verify "<base-ref>^{commit}"` before creation. Don't `pull` into someone else's checkout.

For feature X:

* **Development work:** create/reuse a task branch in its own worktree:
  `git -C "<repo>" worktree add -b "<task-branch>" "<worktree>" "<base-ref>"`
  Use `-b`, not `-B` — `-B` resets the branch and needs explicit authorization. If branch is already checked out elsewhere, reuse that checkout or pick a different branch name.
* **Disposable inspection/testing:** detached HEAD, no branch:
  `git -C "<repo>" worktree add --detach "<worktree>" "<commit>"`
  Anchor anything valuable to a branch before removal.

Default raw-Git location if repo has no convention: `<primary-root>/.worktrees/<task>` with an unused path. Verify with `git rev-parse HEAD` and `status --short --branch` after creation.

What is `<repo>`, desired base, and intended target for feature X?
