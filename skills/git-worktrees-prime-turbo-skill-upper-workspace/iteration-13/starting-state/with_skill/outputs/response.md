No — do not assume `main` is the integration target.

1. **Base vs target:** they may differ. Use your requested base; otherwise inspect the repo's normal target — check docs/config, open PRs, `git worktree list --porcelain -z` and `git rev-parse --verify "<base-ref>^{commit}"`. If you need a current remote base, fetch then resolve before creation.

2. **Feature X implementation:** create a task worktree with a task branch:
`git -C "<repo>" worktree add -b "<task-branch>" "<worktree>" "<base-ref>"`
Reuse the branch for continuation. If it's checked out elsewhere, reuse that checkout or create a different branch — never override checkout protection. Don't use `-B` unless reset is authorized.

3. **Disposable inspection:** use detached HEAD, separate checkout:
`git -C "<repo>" worktree add --detach "<worktree>" "<commit>"`
Anchor any valuable commit to a branch before removal.

No repo in `/tmp/skill-up-1492931976` to verify against — provide: repo path, desired base, integration target, task-branch name, and worktree path to proceed.
