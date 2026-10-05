Place the checkout as a sibling of the bare repo:

```text
/srv/repos/rate-limit
```

Do **not** put it inside `/srv/repos/api.git`. That directory is the shared Git database for a bare repository: objects, refs, config, and worktree admin metadata. A bare repo has no main worktree, so nesting a task checkout there would mix a disposable working tree with repository internals and make repo discovery/backup/cleanup fragile.

Checks/commands in order:

```sh
git -C /srv/repos/api.git rev-parse --is-bare-repository   # expect true
git -C /srv/repos/api.git worktree list --porcelain -z
git -C /srv/repos/api.git rev-parse --verify "<base-ref>^{commit}"

# Only if the task needs a remote base: fetch and resolve that remote ref first.
# Skip `status` because the repo is bare. Skip `check-ignore` because the
# destination is a sibling, not inside another checkout.

git -C /srv/repos/api.git worktree add -b rate-limit /srv/repos/rate-limit "<base-ref>"

git -C /srv/repos/rate-limit rev-parse --show-toplevel
git -C /srv/repos/rate-limit status --short --branch
git -C /srv/repos/rate-limit rev-parse HEAD
git -C /srv/repos/api.git worktree list --porcelain -z
```

Use `-b rate-limit` for a new task branch; use `git show-ref --verify --quiet refs/heads/rate-limit` before continuing an existing branch instead.
