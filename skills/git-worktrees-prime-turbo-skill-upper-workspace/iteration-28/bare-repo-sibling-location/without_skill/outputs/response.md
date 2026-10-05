Place checkout at: `/srv/worktrees/api-rate-limit`

Do not place inside `/srv/repos/api.git`:

* `/srv/repos/api.git` is bare: contains `HEAD,objects/,refs/,config` with `core.bare=true`, no working tree.
* A checkout at e.g. `/srv/repos/api.git/rate-limit` would be stray files inside the object DB, mistaken for internals, subject to `gc/prune`, break push/fetch contract, and not registered as a worktree.

Checks in order, raw `git`, no creation yet:

1. `git --git-dir=/srv/repos/api.git rev-parse --is-bare-repository` -> must be `true`
2. `git --git-dir=/srv/repos/api.git worktree list` -> no conflict, `git --version` supports `worktree`
3. `git --git-dir=/srv/repos/api.git rev-parse --verify <base>` / `branch --list rate-limit` -> resolve base/branch exists
4. `test -e /srv/worktrees/api-rate-limit` -> must not exist; verify target is not under `/srv/repos/api.git/`

Then: `git --git-dir=/srv/repos/api.git worktree add /srv/worktrees/api-rate-limit -b rate-limit <base>`, verify with `worktree list` + `git -C /srv/worktrees/api-rate-limit rev-parse --is-bare-repository` -> `false`.

