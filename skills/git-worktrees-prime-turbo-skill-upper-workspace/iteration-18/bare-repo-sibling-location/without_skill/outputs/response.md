Place checkout outside `GIT_DIR`:

* Exact: `/tmp/opencode/api-rate-limit`
* Never: `/srv/repos/api.git/*` e.g. `/srv/repos/api.git/rate-limit`

Why: `/srv/repos/api.git` is `core.bare=true`, its directory is `$GIT_DIR` (`objects/`,`refs/`,`HEAD`). A checkout inside is inside the object database, will corrupt/fetch breakage, and `git worktree` refuses with `is inside repository`.

Checks, in order, raw Git:

1. `git --git-dir=/srv/repos/api.git rev-parse --is-bare-repository` -> expect `true`
2. `git --git-dir=/srv/repos/api.git worktree list` -> no collision
3. `test ! -e /tmp/opencode/api-rate-limit && realpath` verify target is not under `/srv/repos/api.git`
4. `git --git-dir=/srv/repos/api.git show-ref --verify refs/heads/rate-limit` or `branch --list rate-limit` -> exists or need `-b`
5. `git --git-dir=/srv/repos/api.git worktree add /tmp/opencode/api-rate-limit rate-limit` // add `-b` if new
6. `git --git-dir=/srv/repos/api.git worktree list` + `git -C /tmp/opencode/api-rate-limit rev-parse --show-toplevel`
