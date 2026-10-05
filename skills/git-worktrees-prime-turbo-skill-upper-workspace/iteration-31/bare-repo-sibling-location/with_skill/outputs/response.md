Place at `/srv/repos/api-rate-limit`:

* Sibling of `/srv/repos/api.git`, raw-Git bare-repo fallback: no location convention -> sibling directory.
* Unique, descriptive, unused path for task `rate-limit`.
* Do not use `/srv/repos/api.git/rate-limit` or `/srv/repos/api.git/.worktrees/rate-limit`: `/srv/repos/api.git` is `$GIT_DIR` itself - bare, no working tree. Checkout inside it pollutes objects/refs/admin, breaks `core.bare=true`, risks `gc` deletion.

Checks, in order:

1. `git --git-dir=/srv/repos/api.git rev-parse --is-bare-repository` - confirm bare manager.
2. `git -C "/srv/repos/api.git" worktree list --porcelain -z` - confirm inventory, no conflict.
3. Verify `/srv/repos/api-rate-limit` unused and branch `rate-limit` not checked out elsewhere.
4. Resolve base: inspect integration target, `fetch` if remote, `rev-parse --verify <base>`.
5. Create: `git -C "/srv/repos/api.git" worktree add "/srv/repos/api-rate-limit" -b rate-limit <base>`.
6. Verify: re-list worktrees, `HEAD` commit, path/branch registration.

