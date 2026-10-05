No — do not assume `main` is the integration target.

Verified: `/tmp/skill-up-1440039558` is empty, no git repo to inspect, so no base can be inferred here.

To determine base:

1. `git remote show origin | grep "HEAD branch"`
2. `git branch -a` + check open PRs / `CONTRIBUTING.md` for `main` vs `master` vs `develop` / trunk.
3. `git fetch origin` then base on `origin/<default>`.

Worktree handling:

* Task branch for feature X: persistent, named branch off verified base:
  `git worktree add <path> -b <task-branch> origin/<default>`
  Do work + commit here.
* Disposable inspection checkout: temporary, read-only, never commit:
  `git worktree add --detach <tmp-path> <sha|branch>` then `git worktree remove <tmp-path>` when done.

Provide repo path/URL and desired task-branch name + confirmed integration target if you want me to create it.

