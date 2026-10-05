No — do not assume `main` is the integration target.

Per worktree rules:

* **Base / target:** Use requested base if given. Otherwise inspect repo's normal integration target — check docs/CONTRIBUTING, open PRs, default branch. Do not assume `main`, `master`, `origin`, or current `HEAD`.
* If you need current remote base: `fetch` then resolve ref before creation. Do not `pull` into someone else's checkout.
* **Task branch:** Create a task branch for feature X development; reuse it for continuation. If that branch is already checked out elsewhere, reuse that checkout via owner or create a different branch. Never force-overwrite checkout protection. Don't use `-B` unless reset is authorized.
* **Disposable inspection:** Use detached `HEAD` for inspection/testing only. Anchor any valuable commits to a branch before removal.

To proceed I need: repo path, desired base ref/commit, integration target, and task branch name.
