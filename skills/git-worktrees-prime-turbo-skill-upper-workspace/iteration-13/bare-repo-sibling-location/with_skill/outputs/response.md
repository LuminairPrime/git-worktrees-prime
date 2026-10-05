In raw Git, for `rate-limit`:

* `<repo>`: `/srv/repos/api.git`
* `<worktree>`: `/srv/repos/api-rate-limit` — sibling of bare repo directory.

Do not use `/srv/repos/api.git/rate-limit` or `/srv/repos/api.git/.worktrees/rate-limit`: a bare repository has no main worktree, the directory itself is `$GIT_DIR` (`objects/`, `refs/`, `HEAD`, `config`). A checkout inside it pollutes repository metadata and breaks bare assumptions. No repo convention exists, so per skill use sibling + unique task name.

Checks/creation, in order — not run, no repo attached:

1. `git -C "/srv/repos/api.git" worktree list --porcelain -z` — confirm inventory, no path/branch collision.
2. `git -C "/srv/repos/api.git" rev-parse --verify "<base-ref>^{commit}"` — resolve intended base. Skip `status --short --branch` here: only for non-bare `<repo>`. Skip `check-ignore`: only for destination inside another checkout.
3. Create: `git -C "/srv/repos/api.git" worktree add -b "<task-branch>" "/srv/repos/api-rate-limit" "<base-ref>"`
4. Verify:
   * `git -C "/srv/repos/api-rate-limit" rev-parse --show-toplevel`
   * `git -C "/srv/repos/api-rate-limit" status --short --branch`
   * `git -C "/srv/repos/api-rate-limit" rev-parse HEAD`

