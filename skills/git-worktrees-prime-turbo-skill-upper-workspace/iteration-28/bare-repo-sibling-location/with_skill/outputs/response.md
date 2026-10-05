Placement: sibling of the bare repo:

* Use: `/srv/repos/api-rate-limit` for task `rate-limit`
* From bare repo: `/srv/repos/api.git`

Why not inside:
* `api.git/` is bare metadata only - no `main` checkout. `api.git/rate-limit` or `api.git/.worktrees/rate-limit` mixes work files with `objects/refs/HEAD`, breaks `core.bare`, risks corruption/deletion by `worktree remove/gc`.

Checks, in order:
1. `git -C "/srv/repos/api.git" rev-parse --is-bare-repository` - confirm bare, no `<primary-root>`.
2. `git -C "/srv/repos/api.git" worktree list --porcelain -z` - confirm inventory, that `/srv/repos/api-rate-limit` and branch `rate-limit` are unused/not checked-out elsewhere.
3. Verify path unused: `rate-limit` unique/descriptive, sibling not nested in another disposable worktree. No `check-ignore` needed - not nested.
4. Resolve base: fetch remote if current base required, resolve base ref before create. Do not assume `main/master/origin/HEAD`.
5. Create: `git -C "/srv/repos/api.git" worktree add -b rate-limit "/srv/repos/api-rate-limit" <base>` - use `-b`, never `-B` to avoid reset.
6. Verify: re-`worktree list`, confirm `HEAD`/branch/commit in `/srv/repos/api-rate-limit`.

