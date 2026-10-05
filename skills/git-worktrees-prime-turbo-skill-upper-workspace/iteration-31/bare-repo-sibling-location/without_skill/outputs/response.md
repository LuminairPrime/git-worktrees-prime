Placement: `/tmp/opencode/api-rate-limit`

Do not place inside `/srv/repos/api.git/rate-limit` or similar:
* `/srv/repos/api.git` is bare — directory is the Git DB itself (`HEAD`, `objects/`, `refs/`, `worktrees/`), `core.bare=true`, no working tree.
* Checkout inside would mix work files with object store, risk `gc/prune` damage, break pushes, and conflict with `worktrees/` admin data.

Checks I would run, in order — not run per your no-search constraint:

1. `git --git-dir=/srv/repos/api.git rev-parse --is-bare-repository` — expect `true`
2. `git --git-dir=/srv/repos/api.git worktree list` — no collision / admin lock
3. `git --git-dir=/srv/repos/api.git rev-parse --verify <base-ref>` — base exists
4. `test -e /tmp/opencode/api-rate-limit` — must not exist; parent writable and outside `/srv/repos/api.git`
5. Create: `git --git-dir=/srv/repos/api.git worktree add /tmp/opencode/api-rate-limit -b rate-limit <base>`
6. Verify: `git --git-dir=/srv/repos/api.git worktree list` + `git -C /tmp/opencode/api-rate-limit rev-parse --show-toplevel`

