Do not assume `main` is the integration target.

Empty workspace - `/tmp/skill-up-1786595927` is not a git repo, so no base can be inferred here.

Determine base in the real repo with:

* `git symbolic-ref refs/remotes/origin/HEAD`
* `git branch -r; git remote show origin`
* Target of open PRs and `CONTRIBUTING` / repo docs - often `main`, but can be `develop`, `trunk`, or release branch.

Sync before branching: `git fetch origin`.

Handle branches as:

* Task branch: durable, named, branched from integration base for feature X. Ex: `git worktree add ../feature-x -b feature/x origin/<base>`. Commit, push, open PR from here. Keep until merged.
* Disposable inspection checkout: read-only, no commits. Ex: `git worktree add --detach ../inspect-tmp <sha|branch>`. Delete after with `git worktree remove ../inspect-tmp`.

Provide repo path/URL and feature X name if you want exact commands.
