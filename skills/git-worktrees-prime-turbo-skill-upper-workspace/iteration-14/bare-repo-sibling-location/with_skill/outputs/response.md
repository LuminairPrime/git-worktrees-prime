Place at sibling of bare repo:

`/srv/repos/api-rate-limit`

Why not inside repository directory:

* `/srv/repos/api.git` is bare Git metadata with no working files. `api.git/rate-limit` would nest a checkout inside `objects/refs/worktrees` admin area, polluting the repo, breaking `list/repair/prune` expectations and risking GC/deletion.

Checks I would run, in order:

1. No location convention -> apply bare-repo sibling rule; use unique unused `api-rate-limit`, not inside another worktree.
2. `git -C "/srv/repos/api.git" worktree list --porcelain -z`: confirm no existing `rate-limit` checkout/branch owner.
3. Resolve requested base / normal integration target; do not assume `main/master/HEAD`. If remote base, fetch then resolve ref before creation.
4. Confirm destination unused and outside `/srv/repos/api.git`.
5. Create with `git worktree add` + new `-b rate-limit`, never `-B` / override protection; then re-list to verify path + starting commit.
