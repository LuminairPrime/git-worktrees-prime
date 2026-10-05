Do not assume `main` is the integration target:

* Use requested base, otherwise inspect repo conventions for normal target — do not assume `main`/`master`/`origin`/`HEAD`.
* If remote base required: fetch relevant remote, resolve `rev-parse --verify "<base-ref>^{commit}"` before creation.
* Record: checkout path, branch, starting commit, integration target, manager.

Task branch vs disposable checkout:

* Development `feature X`: new task branch in its own worktree: `git -C "<repo>" worktree add -b "<task-branch>" "<worktree>" "<base-ref>"` — reuse same branch on continuation.
* Disposable inspection/testing: detached HEAD only: `git -C "<repo>" worktree add --detach "<worktree>" "<commit>"` — anchor valuable commits to a branch before removal.

Location: `<primary-root>/.worktrees/<task>` with unique task name, unused path; never inside another disposable worktree, verify ignore coverage if inside a checkout.

