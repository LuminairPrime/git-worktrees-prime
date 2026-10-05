No — do not assume `main` is the integration target.

* `Base` = starting commit/ref. `Integration target` = branch intended to receive it. They may differ — keep both explicit.
* Use requested base; otherwise inspect repo conventions/`origin` to determine normal target. Current dir is not a git repo, so I can't verify it here.
* Feature X: create task worktree with task branch: `git -C "<repo>" worktree add -b "<task-branch>" "<worktree>" "<base-ref>"`
* Disposable inspection/testing only: detached checkout: `git -C "<repo>" worktree add --detach "<worktree>" "<commit>"` — anchor any valuable commit to a branch before removal.
