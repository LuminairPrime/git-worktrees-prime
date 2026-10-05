## Placement

Put the checkout **next to** the bare repository, not inside it:

```
/srv/repos/rate-limit
```

i.e. `/srv/repos/api.git` stays the bare repo, and the task worktree is its sibling directory `/srv/repos/rate-limit` (same parent `/srv/repos`, unique descriptive name, currently unused path).

**Why not inside `/srv/repos/api.git`:** that directory *is* Git's administrative storage for the project — `objects/`, `refs/`, config, and the `worktrees/` metadata that registers linked checkouts. A bare repository has no working tree of its own, so nesting a checked-out working directory inside it mixes the checkout with Git internals: link/registration paths, `gc`/prune, and `core.bare` assumptions all expect the repo dir to contain only administrative data. The "destination inside another checkout" ignore-safety check also cannot apply, because there is no enclosing real checkout in which to configure an ignore rule.

## Checks, in order

1. Inventory existing worktrees and confirm no checkout already owns this task; also confirms the destination is unregistered:
   ```sh
   git -C /srv/repos/api.git worktree list --porcelain -z
   ```
2. Resolve the required base ref (fetch first if a current remote base is needed); a bare repo has no checkout status to inspect:
   ```sh
   git -C /srv/repos/api.git rev-parse --verify "<base-ref>^{commit}"
   ```
3. Confirm the destination path is unused (no existing `/srv/repos/rate-limit`). No `check-ignore` step is needed — it only applies to a destination inside another checkout.
4. Create with a new task branch from that base:
   ```sh
   git -C /srv/repos/api.git worktree add -b rate-limit /srv/repos/rate-limit "<base-ref>"
   ```
5. Verify the resulting checkout and its registration:
   ```sh
   git -C /srv/repos/rate-limit rev-parse --show-toplevel
   git -C /srv/repos/rate-limit status --short --branch
   git -C /srv/repos/rate-limit rev-parse HEAD
   git -C /srv/repos/api.git worktree list --porcelain -z
   ```
