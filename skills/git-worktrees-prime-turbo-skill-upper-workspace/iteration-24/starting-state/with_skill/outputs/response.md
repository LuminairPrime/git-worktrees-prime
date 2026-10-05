Do not assume `main` is the integration target.

* Base vs target are distinct: base = commit/ref you start from, target = branch intended to receive the work. Keep path, branch, starting commit, target explicit.
* If no base requested, inspect repo convention — `CONTRIBUTING`, PR template, default branch, `origin/HEAD` — do not default to `main`/`master`/`origin`/`HEAD`. If current remote base required, fetch then `rev-parse --verify "<base>^{commit}"` before creation.

Task branch vs disposable checkout:

* Development: task worktree + new branch, reuse for continuation:
  `git -C "<repo>" worktree add -b "<task-branch>" "<worktree>" "<base-ref>"`
  If branch already checked out elsewhere, reuse that checkout, don't override protection. Don't use `-B` unless reset authorized.
* Inspection/testing only: detached HEAD, no branch:
  `git -C "<repo>" worktree add --detach "<worktree>" "<commit>"`
  Anchor valuable commits to a branch before removal.

Assumption: no repo in `/tmp/skill-up-2361689558` — only `.opencode/` present — so no worktree created. Provide `<repo>` absolute path, desired `<base-ref>`, integration target, and `<task-branch>` + `<worktree>` path to proceed.
