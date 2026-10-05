Place checkout at `/tmp/opencode/api-rate-limit`.

Why not inside `/srv/repos/api.git/`:

* `/srv/repos/api.git` is bare: contains `HEAD, objects/, refs/, config`, no working tree.
* `git` refuses linked worktree nested inside `$GIT_DIR`: contaminates metadata, risks `gc/prune` damage, breaks bare push/pull assumptions.

Checks, in order:

1. `git --git-dir=/srv/repos/api.git rev-parse --is-bare-repository` — must print `true`.
2. `git --git-dir=/srv/repos/api.git worktree list` — confirm no existing `rate-limit` worktree/path collision.
3. `test -e /tmp/opencode/api-rate-limit` — must not exist; `test -d /tmp/opencode -a -w /tmp/opencode` — parent exists/writable.
4. Create: `git --git-dir=/srv/repos/api.git worktree add /tmp/opencode/api-rate-limit -b rate-limit`.
