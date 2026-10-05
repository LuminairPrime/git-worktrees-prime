## Placement

**`/srv/repos/rate-limit`** — a sibling of the repository directory `/srv/repos/api.git` (equally acceptable: `/srv/repos/api-rate-limit`).

There is no repository location convention to follow, so the fallback applies: `<primary-root>/.worktrees/<task>` for a normal repo, but a bare repository has **no main worktree and therefore no `<primary-root>`** — the fallback becomes a *sibling of the repository directory*. Use a unique, descriptive, currently unused path.

## Why not inside `/srv/repos/api.git`

1. That directory is not a checkout — it is the repository's storage (objects, refs, `hooks/`, `packed-refs`, the `worktrees/` admin area). A worktree there would mix your task's working files into the very directory Git writes to during `gc`/`repack`/ref updates.
2. The inverse risk: `git worktree remove`, `prune`, or deleting/renaming the bare repo would target a directory containing your task files — cleanup of the repo becomes data loss for the task, and moving the repo would break the worktree registration.
3. It collapses the boundary the worktree exists to create: the checkout's `.git` file points back at the storage dir, so "task files" and "repo internals" would live in one tree with no way to remove one without touching the other.

## Checks, in order (raw Git)

```sh
# 1. Confirm the source is a bare repository (and a repository at all).
git -C /srv/repos/api.git rev-parse --is-bare-repository          # expect: true

# 2. Inventory registrations: bare repo has no main worktree;
#    confirm no checkout already exists for this task, path is unused.
git -C /srv/repos/api.git worktree list --porcelain -z

# 3. Resolve the base explicitly. Do NOT assume main/master/origin/HEAD.
git -C /srv/repos/api.git rev-parse --verify "<base-ref>^{commit}"

# 4. Destination must not exist.
test ! -e /srv/repos/rate-limit

# 5. Create with a task branch (-b, never -B), based on the resolved commit.
git -C /srv/repos/api.git worktree add -b rate-limit /srv/repos/rate-limit "<base-ref>"

# 6. Verify the checkout.
git -C /srv/repos/rate-limit rev-parse --show-toplevel   # must print /srv/repos/rate-limit
git -C /srv/repos/rate-limit status --short --branch     # correct branch, clean
git -C /srv/repos/rate-limit rev-parse HEAD              # must equal step 3's commit

# 7. Verify the registration.
git -C /srv/repos/api.git worktree list --porcelain -z
```

Notes: the `check-ignore` step does **not** apply here — it is required only when creating *inside another checkout*, and this destination is a sibling of the bare repo, not inside any checkout. No `status` check on step 1's source: bare repositories have no working tree.
