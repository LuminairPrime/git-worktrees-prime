No — you can't remove it first. A detached HEAD's commits have **no branch reference**; they are only held by the checkout's `HEAD` reflog. Delete the checkout (especially with `rm -rf`, which bypasses Git entirely) and you're relying on reflog expiry windows (`gc.reflogExpire`, 90 days default) to get them back. Rescue them first, in this order.

## Checks (run inside the disposable checkout)

```bash
git status                 # confirm detached HEAD, no uncommitted changes
git status --porcelain     # must be empty; if not, see step 5
git rev-parse HEAD         # record the tip SHA — save this output
git log --oneline -5       # identify your three commits
```

Confirm they exist nowhere else:

```bash
git branch -a --contains <TIP_SHA>          # expect empty output
git log --oneline main..<TIP_SHA>           # should list exactly your three
git stash list                              # nothing valuable hiding here either
```

## Rescue: attach the commits

From inside the checkout (fastest, gives them a proper ref):

```bash
git switch -c inspection-backup             # branch now points at <TIP_SHA>
```

Or from the parent repo, without touching the checkout:

```bash
git branch inspection-backup <TIP_SHA>
```

## Verify the reference exists

```bash
git branch --contains <TIP_SHA>             # must now print inspection-backup
git log --oneline -3 inspection-backup
git merge-base --is-ancestor <TIP_SHA> main && echo reachable  # optional
```

Only when `<TIP_SHA>` shows up in `git branch --contains` are the commits independent of the checkout.

## Integrate into a real branch (if you haven't already)

```bash
git switch main
git merge --ff-only inspection-backup       # or: cherry-pick / rebase
git log --oneline -5                        # confirm the three landed
```

## Then remove the checkout

If it's a linked worktree:

```bash
git worktree list                 # find its path
git worktree remove <path>        # add --force only if it's still dirty
git worktree prune                # clean up stale metadata
```

If it was a plain detached checkout in its own directory:

```bash
git switch main                    # leave detached state
# then delete the directory with your normal file tooling
git reflog expire --expire=now --all   # only if you must purge it immediately
```

Only after step "Verify the reference exists" is it safe to delete. And keep `git branch inspection-backup` around until you've confirmed the merge in `git log` — it costs nothing and doubles as your rollback point.

## If you already removed it

```bash
git reflog                         # find the old HEAD position
git fsck --unreachable --no-reflogs # list dangling commits
git branch rescue <SHA>            # re-attach anything valuable
```
