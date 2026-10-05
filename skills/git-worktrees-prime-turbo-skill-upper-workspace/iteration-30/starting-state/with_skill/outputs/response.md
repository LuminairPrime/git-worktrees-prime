No git repo in `/tmp/skill-up-2757557758` — only `.opencode/`, so no worktree created yet.

For feature X:

1. **Do not assume `main` is the integration target.**
   Use the requested base; otherwise inspect repo conventions (default branch, CONTRIBUTING, open PRs) to find the normal target. If a current remote base is required: fetch then resolve `rev-parse --verify "<base-ref>^{commit}"` before creation. Don't `pull` into someone else's checkout.

2. **Task branch for development:**
   `git -C "<repo>" worktree add -b "<task-branch>" "<worktree>" "<base-ref>"`
   Reuse the same branch for continuation. If it's checked out elsewhere, reuse that checkout or pick a different branch. Don't use `-B` unless reset is authorized.

3. **Disposable inspection only:**
   `git -C "<repo>" worktree add --detach "<worktree>" "<commit>"`
   Anchor any valuable detached commit to a branch before removal.

Location default (raw Git): `<primary-root>/.worktrees/<task>` with unused path, verified with `worktree list --porcelain -z` and `check-ignore -q`.

To proceed I need: repo path, integration target, base ref, task-branch + worktree name.
