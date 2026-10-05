No — do not assume `main` is the integration target.

Per worktree skill:

* **Base / integration target:** Use the requested base. If none was given, inspect the repo's normal target — `CONTRIBUTING`, PR template, default branch, open PRs — do not default to `main`/`master`/`origin`/`HEAD`.
* If a current remote base is required: fetch that remote and resolve the ref before creation. Do not `pull` into someone else's checkout.
* Record: checkout path, branch, starting commit, integration target, manager.

**Task branch vs disposable checkout:**

* **Implement feature X:** create a task branch for development with `git worktree add -b`. Reuse it on continuation.
* If that branch is already checked out elsewhere, reuse that checkout via its owner or create a different branch from the required commit. Never override checkout protection; do not use `-B` unless branch reset is authorized.
* **Disposable inspection/testing:** use detached `HEAD`. Anchor any valuable detached commits to a branch before removal.
