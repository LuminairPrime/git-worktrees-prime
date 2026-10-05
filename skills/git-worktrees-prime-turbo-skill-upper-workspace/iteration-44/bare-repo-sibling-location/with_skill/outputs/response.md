## Placement

```
/srv/repos/rate-limit          ← checkout (sibling of /srv/repos/api.git)
/srv/repos/api.git             ← bare repo stays untouched
/srv/repos/api.git/worktrees/rate-limit   ← Git's admin registration (created for you)
```

With no repository convention to follow, the rule is: **`<primary-root>/.worktrees/<task>` when a main worktree exists; a sibling of the repository directory when the repository is bare.** A bare repository has no main worktree, so there is no primary root — use the sibling: `/srv/repos/rate-limit`.

### Why not inside `/srv/repos/api.git`

- That directory *is* the Git directory (objects, refs, hooks, `packed-refs`) — administrative storage, not a working area. A checkout's files, index, and `HEAD` would be mixed into storage that Git and repo-level tooling treat as metadata-only.
- Git keeps linked-worktree metadata at `<gitdir>/worktrees/<name>/`. A checkout directory living alongside that hierarchy is indistinguishable from Git's own bookkeeping and can collide with it.
- Repo-level operations (gc, prune, backups, mirrors that `rsync`/delete the `.git` dir) would then touch your task's working files — a `git worktree prune` cycle or a repo cleanup could destroy live work, and conversely your untracked build output pollutes the repository directory.
- There is no enclosing checkout to ignore against: a bare repo has no working tree, so `.gitignore`/`check-ignore` protection is impossible there. (Also: never place it inside another disposable worktree.)

## Checks, in order

```sh
# 1. Confirm the repository exists and is bare.
git -C /srv/repos/api.git rev-parse --is-bare-repository        # require: true

# 2. Inventory existing registrations; confirm no rate-limit checkout/branch is in use.
git -C /srv/repos/api.git worktree list --porcelain -z

# 3. Determine the base from the repo itself — do not assume main/master.
git -C /srv/repos/api.git symbolic-ref HEAD
git -C /srv/repos/api.git rev-parse --verify "<base-ref>^{commit}"

# 4. Confirm the destination path is unique/unused.
test ! -e /srv/repos/rate-limit

# 5. (Not applicable) check-ignore is only for destinations inside another
#    checkout; a bare repository has none.

# 6. Create: new task branch, explicit base.
git -C /srv/repos/api.git worktree add -b rate-limit /srv/repos/rate-limit "<base-ref>"

# 7. Verify the resulting checkout.
git -C /srv/repos/rate-limit rev-parse --show-toplevel           # expect /srv/repos/rate-limit
git -C /srv/repos/rate-limit status --short --branch             # on rate-limit, clean
git -C /srv/repos/rate-limit rev-parse HEAD                      # matches step 3's base commit

# 8. Re-list registrations to confirm the new worktree is recorded.
git -C /srv/repos/api.git worktree list --porcelain -z
```

If instead the checkout had already been moved or renamed, step 2 would be preceded by `git -C /srv/repos/api.git worktree repair "/srv/repos/rate-limit"` (current absolute path) before any `cd`, `status`, or listing.
