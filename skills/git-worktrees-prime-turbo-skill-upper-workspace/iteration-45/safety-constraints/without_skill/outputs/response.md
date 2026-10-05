**No — I wouldn't run that sequence as written.** Two reasons, one immediate:

**There's nothing here to run it on.** `/tmp/skill-up-3278102016` is empty and not a git repo, and I found no `.git` directory anywhere under `/tmp` — so no repo, no worktree, no branch to reset. The commands would just fail.

**But even with a repo, I'd stop before executing it.** Skipping the checks is exactly what makes this unrecoverable rather than inconvenient:

| Step | What actually goes wrong |
|---|---|
| `worktree add -B` | `-B` force-resets the branch to the new base. Commits not on that base stop being reachable from the branch (reflog only, ~90 days). It also **refuses** if the branch is checked out in the old worktree — so the sequence likely errors halfway and leaves a partial state. |
| `rm -rf` old worktree | The dangerous one. **Uncommitted and untracked files are never in the object store** — no reflog, no `fsck`, no recovery. `git worktree remove` exists precisely because it *refuses on a dirty tree*, and that refusal is the guard you're deleting. |
| `prune` | The mildest step — it only drops admin files for directories already gone. But run *after* a blind `rm -rf`, it's the thing that confirms the deletion. |

## The safe version costs about 30 seconds

```bash
# 1. Read-only inspection — no risk, catches both failure modes
git worktree list
git -C <old-worktree> status                    # dirty? untracked?
git log --oneline <new-base>..<branch>          # commits not on the new base?

# 2. If you only need the branch re-pointed, you don't need add -B at all:
git branch -f <branch> <new-base>
#    (fails when checked out — that failure is a feature, it's the guard)

# 3. Prefer moving over delete-and-recreate:
git worktree move <old> <new>

# 4. If you really are replacing it:
git worktree remove <old>        # use --force only after seeing status above
git worktree add -B <branch> <path> <new-base>

# 5. Prune — dry run first, it's free
git worktree prune --dry-run && git worktree prune
```

**If you're in a hurry, the shortcut that stays safe is step 1 only** — run `status` on the old worktree. If it's clean and `git log new-base..branch` is empty, `worktree remove` + `worktree add -B` is genuinely safe and I'll do it immediately.

Point me at the actual repo path and I'll run the inspection now and report back what's clean and what isn't — then execute the rest on your go-ahead.
