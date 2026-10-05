Place at `/srv/repos/api-rate-limit` — sibling of the bare repo, outside `GIT_DIR`.

Why not `/srv/repos/api.git/rate-limit`:
* `/srv/repos/api.git` is `core.bare=true` with no working tree. Anything inside it is treated as Git internals.
* Would pollute `objects/`, `refs/`, `worktrees/` admin dir, risk `gc/prune` damage, break pushes, and break `git-common-dir` linkage.

Checks in order:

1. `git --git-dir=/srv/repos/api.git rev-parse --is-bare-repository` -> must be `true`
2. `git --git-dir=/srv/repos/api.git worktree list --verbose` -> no existing `rate-limit` entry/path collision
3. `test ! -e /srv/repos/api-rate-limit` -> target must not exist, and is not prefixed by `/srv/repos/api.git/`
4. `git --git-dir=/srv/repos/api.git branch --list rate-limit` -> decide `-b rate-limit` vs. attach existing
5. Create: `git --git-dir=/srv/repos/api.git worktree add /srv/repos/api-rate-limit -b rate-limit`
6. Verify: `git -C /srv/repos/api-rate-limit rev-parse --show-toplevel --git-common-dir --is-bare-repository` -> `/srv/repos/api-rate-limit`, `/srv/repos/api.git`, `false`
7. `git --git-dir=/srv/repos/api.git worktree list` + `git -C /srv/repos/api-rate-limit status --short --branch`

