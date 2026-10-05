Placement: `/srv/repos/api-rate-limit`

* Bare repository has no `<primary-root>`: use sibling of repository directory.
* No location convention exists.
* Do not place inside `/srv/repos/api.git`: that directory is the Git store (`objects/`, `refs/`, etc.), not a checkout. A checkout inside would contaminate the bare store.

Checks, in order — do not create until all pass:

1. `git -C /srv/repos/api.git worktree list --porcelain -z`: confirm no checkout already owns `rate-limit`, confirm branch availability.
2. Verify destination unused and unique: `/srv/repos/api-rate-limit` does not exist, is not inside another disposable worktree.
3. Resolve base / integration target: do not assume `main`/`master`/`origin`/`HEAD`; fetch remote and resolve ref first if current remote base required.
4. Create with raw Git from `<repo>=/srv/repos/api.git` to exact `<worktree>=/srv/repos/api-rate-limit` with task branch via `-b`, never `-B` / never override checked-out branch.
5. Verify after creation: returned path/commit, re-list `worktree list`, record path/branch/starting commit/target.
