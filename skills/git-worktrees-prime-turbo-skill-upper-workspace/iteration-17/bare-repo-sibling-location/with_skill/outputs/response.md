Placement: `/srv/repos/api-rate-limit` — sibling of `/srv/repos/api.git`.

Why:

* No location convention -> raw Git fallback is sibling of repository directory for bare repo.
* Do not use `/srv/repos/api.git/rate-limit` or `/srv/repos/api.git/.worktrees/rate-limit`: a bare repo has no working tree, `core.bare=true`. Placing files inside it mixes checkout with `objects/refs/config` and worktree metadata.

Checks, in order — would run, not ran:

1. Confirm manager/location: no harness, no repo convention -> raw Git sibling rule applies, name `api-rate-limit` unique/descriptive, path unused.
2. `git -C "/srv/repos/api.git" worktree list --porcelain -z` — confirm no existing `rate-limit` checkout/branch collision.
3. Verify destination does not exist and parent `/srv/repos` writable.
4. Resolve base/integration target, `git rev-parse` base; create with `git worktree add -b <branch> <worktree> <base>`, never `-B` without reset authorization.
5. Verify: re-list with `worktree list --porcelain -z`, confirm returned path/commit.

