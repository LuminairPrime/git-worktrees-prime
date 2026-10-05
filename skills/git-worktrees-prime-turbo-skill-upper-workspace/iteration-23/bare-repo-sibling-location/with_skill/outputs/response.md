Place at sibling of bare repo: `/srv/repos/api-rate-limit`.

Why not inside `/srv/repos/api.git`: that path is the bare `GIT_DIR` itself (`objects/`, `refs/`, `HEAD`, `config`) — no main worktree. Nesting a checkout there puts working files inside Git admin data, risks corruption/GC/prune confusion, not a registered linked-worktree location. Bare has no `<primary-root>/.worktrees/<task>`; fallback is sibling.

Checks, in order:

1. `git -C "/srv/repos/api.git" worktree list --porcelain -z`: confirm no existing `rate-limit` checkout/owner, branch reuse.
2. Verify unused absolute path: `/srv/repos/api-rate-limit` must not exist; parent `/srv/repos` writable.
3. Resolve base/integration target: do not assume `main/master/origin/HEAD`; fetch remote + resolve ref if current base required.
4. Read Creation commands, then create: `git -C "/srv/repos/api.git" worktree add -b <branch> "/srv/repos/api-rate-limit" <base>`.
5. Verify: re-list `worktree list --porcelain -z`, `rev-parse --abbrev-ref HEAD` + tip commit from new checkout.
6. No `check-ignore`/exclude check — only required when nesting inside another checkout.

