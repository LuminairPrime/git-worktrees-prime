## Placement

```
/srv/repos/api-rate-limit
```

A **sibling** of the bare repository, outside it, named `<repo>-<task>` so it doesn't collide with other repos' worktrees:

- Repo (git dir): `/srv/repos/api.git`
- Worktree (checkout): `/srv/repos/api-rate-limit`
- Git's admin metadata: `/srv/repos/api.git/worktrees/rate-limit` (created automatically)

If you'd rather keep `/srv/repos` purely for repo storage, use a parallel top-level tree instead — `/srv/worktrees/api-rate-limit`. Either is fine; what matters is that the checkout is **not** under `/srv/repos/api.git`.

## Why not inside the repository directory

`/srv/repos/api.git` *is* the `$GIT_DIR` — it contains `objects/`, `refs/`, `HEAD`, `config`, `hooks/`, `packed-refs`, and the administrative `worktrees/` area. Putting a checkout in there mixes working files into storage:

1. **It pollutes the object store's parent.** The checkout's files land next to `objects/` and `refs/`, so any tool that walks, packs, or mirrors that directory drags the checkout along.
2. **Backups and clones become wrong.** `git clone --mirror /srv/repos/api.git`, `git bundle`, `rsync`/`tar` of the repo dir, or a server migration would copy the working tree into the mirror — or into `objects/`' neighborhood.
3. **Self-reference.** Git stores the worktree's metadata in `/srv/repos/api.git/worktrees/rate-limit`, whose `gitdir` file points back up at the checkout. Nesting the checkout *under* the directory that holds its own metadata creates a recursive path — file watchers, IDE indexing, and recursive tooling can loop or mis-index.
4. **Cleanup hazards.** `git clean -xdf` (or any command run with `GIT_DIR=/srv/repos/api.git` plus a work tree) would target the checkout from inside the repo's storage. A bare repo is supposed to be safe from work-tree operations; nesting a work tree removes that safety.
5. **Serving/hooks noise.** Bare repos are often exposed via `git daemon`, dumb HTTP, or shared hosting hooks; stray directories in the served namespace are at best confusing and at worst leak source code.

A bare repo has no work tree by design, so the checkout has to live somewhere — "somewhere else" is the rule, not "here."

## Checks, in order

```bash
# 1. Confirm it's bare and has no work tree (no repo attached — this validates the premise)
git -C /srv/repos/api.git rev-parse --is-bare-repository   # expect: true
git -C /srv/repos/api.git rev-parse --show-toplevel        # expect: fatal (no work tree)

# 2. Confirm GIT_DIR resolves where you think it does
git -C /srv/repos/api.git rev-parse --git-dir --git-common-dir
#   expect: /srv/repos/api.git (both)

# 3. Confirm the destination is outside the repo dir and free
case "$(realpath /srv/repos/api-rate-limit 2>/dev/null || echo n/a)" in
  /srv/repos/api.git*) echo "INSIDE REPO — refuse"; exit 1;;
esac
test ! -e /srv/repos/api-rate-limit || { echo "path exists"; exit 1; }

# 4. Baseline the worktree list
git -C /srv/repos/api.git worktree list

# 5. Resolve the task ref (branch, else the commit you'll branch from)
git -C /srv/repos/api.git rev-parse --verify refs/heads/rate-limit
#   if missing: note the base commit instead, e.g. refs/heads/main

# 6. Create it
git -C /srv/repos/api.git worktree add /srv/repos/api-rate-limit rate-limit
#   if branch didn't exist in step 5:
#   git -C /srv/repos/api.git worktree add -b rate-limit /srv/repos/api-rate-limit main

# 7. Verify linkage: checkout points at the bare repo's admin area, not a new .git dir
git -C /srv/repos/api-rate-limit rev-parse --show-toplevel   # /srv/repos/api-rate-limit
git -C /srv/repos/api-rate-limit rev-parse --git-dir         # /srv/repos/api.git/worktrees/rate-limit
git -C /srv/repos/api-rate-limit branch --show-current       # rate-limit

# 8. Verify the bare dir gained only the admin entry, no checkout files
git -C /srv/repos/api.git worktree list                     # both entries, correct paths
ls /srv/repos/api.git                                       # objects refs hooks config HEAD ... worktrees only

# 9. Housekeeping sanity
git -C /srv/repos/api.git worktree prune --dry-run          # expect: no output
```

The critical assertions are #7 (metadata lives under `$GIT_DIR/worktrees/`, checkout lives outside) and #8 (nothing new inside the bare dir besides `worktrees/rate-limit`).
