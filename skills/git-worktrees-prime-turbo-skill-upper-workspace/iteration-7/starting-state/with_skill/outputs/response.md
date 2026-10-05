No — do not assume `main` is the integration target.

Per worktree rules: use requested base, otherwise inspect repo's normal target. `main`/`master`/`origin`/`HEAD` are not valid defaults.

Current state: `/tmp/skill-up-2307089645` contains only `.opencode/` — no repo, so base/target cannot be resolved here.

Handle branches as:

* Feature X implementation: task branch, created from selected base:
`git -C "<repo>" worktree add -b "<task-branch>" "<worktree>" "<base-ref>"`
Reuse for continuation; if checked out elsewhere, reuse that checkout, don't override.
* Disposable inspection/testing: detached HEAD:
`git -C "<repo>" worktree add --detach "<worktree>" "<commit>"`
Anchor valuable commits to a branch before removal.

To proceed I need:
1. Repo path (`<repo>`)
2. Requested base ref/commit, or authority to detect it
3. Intended integration target branch
4. Task branch + worktree name
