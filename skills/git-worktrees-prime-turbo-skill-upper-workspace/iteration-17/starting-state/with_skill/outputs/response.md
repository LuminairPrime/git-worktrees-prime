Do not assume `main` is the integration target.

* **Base vs target are separate:** base = commit/ref you start from, target = branch to receive the work. Keep both explicit.
* **Determine both from repo conventions:** check README/CONTRIBUTING, open PRs, default branch, or ask. If you need current remote state: fetch then resolve `<base-ref>^{commit}` before creating.

For this request in `/tmp/skill-up-1289563255` — not a git repo — provide: repo path, desired base, integration target, and task name.

**Task branch vs disposable checkout:**

* **Implement feature X:** new worktree + new branch:
  `git -C "<repo>" worktree add -b "<task-branch>" "<worktree>" "<base-ref>"`
  Reuse the branch for continuation. If already checked out elsewhere, reuse that checkout or use a different branch name. Do not use `-B` unless branch reset is authorized.
* **Disposable inspection/testing:** detached HEAD, no branch:
  `git -C "<repo>" worktree add --detach "<worktree>" "<commit>"`
  Anchor any valuable commit to a branch before removal.

Default location for raw Git: `<primary-root>/.worktrees/<task>` with unused path; verify with `git worktree list --porcelain -z`.

