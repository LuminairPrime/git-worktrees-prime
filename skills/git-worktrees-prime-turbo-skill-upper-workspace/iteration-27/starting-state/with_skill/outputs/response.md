No — do not assume `main` is the integration target.

* **Base:** use your requested base. If none, inspect the repo conventions — default branch, CONTRIBUTING, PR template — `main`/`master`/`origin`/`HEAD` are not automatically correct.
* If you need a current remote base, fetch that remote and resolve `<base-ref>^{commit}` before creating.
* Keep base and integration target explicit — they may differ.

For feature X implementation vs inspection:

* **Task work:** new branch explicitly based on commit:
  `git -C "<repo>" worktree add -b "<task-branch>" "<worktree>" "<base-ref>"`
  Reuse that branch/checkout for continuation. If already checked out elsewhere, reuse it or use a different branch — never override. Don't use `-B` unless reset is authorized.
* **Disposable inspection/testing:** detached HEAD:
  `git -C "<repo>" worktree add --detach "<worktree>" "<commit>"`
  Anchor valuable commits to a branch before removal.

Current dir `/tmp/skill-up-93144203` is not a git repo, so I can't resolve a base here. Provide: repo path, desired base + integration target, task-branch name, and worktree path/manager to create it.
