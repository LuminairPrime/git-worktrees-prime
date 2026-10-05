## Placement

Put the checkout as a **sibling of the bare repository directory**, e.g.:

```
/srv/repos/rate-limit
```

(i.e. `/srv/repos/api.git`'s parent directory holds the sibling `rate-limit/`). The convention's fallback `<primary-root>/.worktrees/<task>` does not apply here because a bare repository has no main worktree / primary root, so the sibling placement is the designated option.

**Why not inside `/srv/repos/api.git`:** that directory *is* the Git administrative directory itself (HEAD, config, objects/, refs/). A worktree placed inside it would nest working files among Git's own metadata, risk being mistaken for repository internals, cannot be excluded via `.gitignore`/`info/exclude` the way a nested path in a real checkout can, and makes later `worktree remove`/`repair`/prune fragile.

## Checks, in order (no repo present, so run these when it is)

1. **Confirm it's bare and inventory worktrees** (expect no linked worktrees; confirm `rate-limit` isn't already registered to another worker):
   - `git -C /srv/repos/api.git rev-parse --is-bare-repository`
   - `git -C /srv/repos/api.git worktree list --porcelain -z`
2. **Determine branch status** — don't assume `main`/`master`:
   - `git -C /srv/repos/api.git branch -v`
   - `git -C /srv/repos/api.git symbolic-ref HEAD`
   - `git -C /srv/repos/api.git show-ref --verify --quiet refs/heads/rate-limit` (exit 0 → reuse branch; non-zero → create with `-b`)
3. **Resolve and verify the base ref** (fetch the remote first if a current base is required; do not pull into someone else's checkout):
   - `git -C /srv/repos/api.git rev-parse --verify "<base-ref>^{commit}"`
4. **Verify the destination is unique and unused** (sibling, so not inside another checkout — the `check-ignore` step is not needed since the bare repo is not a checkout):
   - `test ! -e /srv/repos/rate-limit`
5. **Create** (new branch from the selected base):
   - `git -C /srv/repos/api.git worktree add -b rate-limit /srv/repos/rate-limit <base-ref>`
   - (or `worktree add /srv/repos/rate-limit rate-limit` if reusing the existing branch; `--detach` only for disposable inspection)
6. **Verify the checkout and registration**:
   - `git -C /srv/repos/rate-limit rev-parse --show-toplevel`
   - `git -C /srv/repos/rate-limit status --short --branch`
   - `git -C /srv/repos/rate-limit rev-parse HEAD` (matches base)
   - `git -C /srv/repos/api.git worktree list --porcelain -z`
