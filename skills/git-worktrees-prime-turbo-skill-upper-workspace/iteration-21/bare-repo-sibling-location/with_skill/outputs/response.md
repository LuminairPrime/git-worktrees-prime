Place at `/srv/repos/api-rate-limit`:

* Sibling of `/srv/repos/api.git` — raw-Git fallback when no location convention exists.
* Unique `api-rate-limit`: preserves repo + task, unused path.
* Not inside `/srv/repos/api.git/`: bare directory contains `objects/`, `refs/`, `config` only, no working tree. Checkout files there would pollute/corrupt bare internals.

Checks, in order:

1. Confirm bare: `git -C "/srv/repos/api.git" rev-parse --is-bare-repository`
2. Inventory: `git -C "/srv/repos/api.git" worktree list --porcelain -z` — confirm path/branch, no collision, no other owner for task
3. Confirm destination unused: path not in list output and `test -e /srv/repos/api-rate-limit` is false
4. Resolve intended base ref before `worktree add`; create with `<repo>`=`/srv/repos/api.git`, `<worktree>`=`/srv/repos/api-rate-limit`
5. Verify after: re-list worktrees, confirm absolute path + starting commit
