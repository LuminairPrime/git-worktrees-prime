Placement: ` /srv/repos/api-rate-limit` — sibling of `/srv/repos/api.git`.

Why: raw Git rule with no repo convention is `<primary-root>/.worktrees/<task>`, or sibling of repository directory for bare repo. Never inside `/srv/repos/api.git`: bare repo has no working files, only objects/refs/admin — checkout inside it pollutes repo storage and risks GC/prune/deletion.

Checks, in order:

1. Confirm ` /srv/repos/api.git` is the bare manager.
2. `git -C "/srv/repos/api.git" worktree list --porcelain -z`: confirm no existing `rate-limit` checkout/branch owner.
3. Confirm `/srv/repos/api-rate-limit` is unused, not inside another disposable worktree.
4. Resolve base/integration target and task branch; do not assume `main`/`origin`/`HEAD`.
5. Read Creation commands before `git worktree add "<repo>" "<worktree>"` with exact absolute paths.
6. After creation: verify returned path/commit, re-list worktrees.
