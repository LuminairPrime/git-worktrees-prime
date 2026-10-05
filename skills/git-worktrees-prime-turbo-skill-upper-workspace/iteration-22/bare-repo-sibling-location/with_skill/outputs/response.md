Placement: `/srv/repos/rate-limit` — sibling of `/srv/repos/api.git` under `/srv/repos/`.

Why:
- No location convention -> bare repo rule: sibling of repository directory.
- Never inside `/srv/repos/api.git`: bare directory is `$GIT_DIR` only, no main worktree. Checkout inside would mix work files with objects/refs/config and break registration/bare-ness.

Checks, in order:
1. Confirm manager=`raw Git`, base/integration target — do not assume `main`/`master`/`origin`/`HEAD`.
2. Verify unused path `/srv/repos/rate-limit` and unused branch `rate-limit`: `git --git-dir=/srv/repos/api.git worktree list --porcelain -z`, `branch --list rate-limit`.
3. If current remote base required: fetch relevant remote, resolve ref to commit before creation.
4. Create: `git -C /srv/repos/api.git worktree add -b rate-limit /srv/repos/rate-limit <base-commit>` — never `-B` / override protection.
5. Verify: returned path, `HEAD` commit, branch, `worktree list` registration.
