In `/tmp/skill-up-3462026202`: not a git repo, so don't assume `main`.

1. Determine base, don't assume:
```sh
git fetch origin
git symbolic-ref refs/remotes/origin/HEAD # -> origin/main, origin/develop, etc.
git branch -r | head -20
```
Use `origin/<default>` as base unless `CONTRIBUTING` / open PRs show otherwise (e.g. `develop`, `trunk`, `release/*`).

2. Task branch (for feature X) - persistent, committable:
```sh
git worktree add ../repo-feature-x -b feat/x origin/main
# work there, commit, push, PR to integration target
git worktree list
```

3. Disposable inspection - read-only, detach, delete after:
```sh
git worktree add --detach /tmp/repo-inspect origin/main
# inspect, then:
git worktree remove /tmp/repo-inspect --force; git worktree prune
```

Rule: one task branch per feature, never commit in detached checkout.

Provide your repo path/URL if you want me to create it.
