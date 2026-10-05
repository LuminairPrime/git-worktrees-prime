Placement: `/srv/repos/rate-limit`

Why:
* No location convention -> bare-repository rule: sibling of repository directory.
* ` /srv/repos/api.git` is the bare `GIT_DIR` itself, no `<primary-root>`. ` <primary-root>/.worktrees/<task>` does not apply.
* Do not place inside `/srv/repos/api.git`: would mix checkout files with objects/refs/metadata, break bare-ness, registration/`gc`/prune.

Checks, in order, no filesystem search:
1. Read `references/raw-git-commands.md#creation` before `add`.
2. `git -C "/srv/repos/api.git" worktree list --porcelain -z`: confirm no existing `rate-limit` checkout/owner.
3. Confirm `/srv/repos/rate-limit` unused and unregistered; confirm task branch not checked out elsewhere.
4. Resolve base/integration target from repo norm, fetch remote ref if needed; do not assume `main`/`master`/`HEAD`.
5. Create with `git -C "<repo>" worktree add` + new `rate-limit` branch, then re-`list` to verify path/commit/registration.

