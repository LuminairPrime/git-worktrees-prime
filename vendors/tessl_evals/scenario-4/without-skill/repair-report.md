# Worktree Registration Repair Report

## Summary

A linked Git worktree for the `feature/data-pipeline` branch was physically relocated
with `mv` (simulating a file-manager move) from its original location to a new one,
without telling Git. Git's administrative records still pointed at the old path, so the
worktree appeared as `prunable` and the branch looked detached from its checkout. The
registration was restored with `git worktree repair`; the checkout is now correctly
registered at its current location and the feature branch work is intact.

## Paths involved

| Role | Path |
|------|------|
| Main worktree / repository | `/workspace/solution/repo` |
| Original (stale) worktree path | `/workspace/solution/repo/.worktrees/data-pipeline` |
| Current (actual) worktree path | `/workspace/solution/repo/.worktrees/pipeline-v2` |
| Worktree admin directory (main repo) | `/workspace/solution/repo/.git/worktrees/data-pipeline` |
| Stale pointer file that was wrong | `/workspace/solution/repo/.git/worktrees/data-pipeline/gitdir` |

The admin directory under `.git/worktrees/` is named `data-pipeline` after the worktree's
*original* directory name. Git does not rename this directory when a worktree moves; only
the `gitdir` pointer inside it needs to be updated.

## Before the fix — what Git reported

`git worktree list` (run from `/workspace/solution/repo`):

```
/workspace/solution/repo                          12629ff [master]
/workspace/solution/repo/.worktrees/data-pipeline a4f5b32 [feature/data-pipeline] prunable
```

`git worktree list --porcelain`:

```
worktree /workspace/solution/repo
HEAD 12629ffc1030db8306cdcc25ec4ac7e593d089e5
branch refs/heads/master

worktree /workspace/solution/repo/.worktrees/data-pipeline
HEAD a4f5b320e97aaedb0207e06f62cb91c9685ae3ae
branch refs/heads/feature/data-pipeline
prunable gitdir file points to non-existent location
```

The stale pointer file contained the old, now-nonexistent location:

```
$ cat /workspace/solution/repo/.git/worktrees/data-pipeline/gitdir
/workspace/solution/repo/.worktrees/data-pipeline/.git
```

The checkout itself, meanwhile, was sitting at the new location with a `.git` file that
still correctly pointed *back* to the main repository:

```
$ cat /workspace/solution/repo/.worktrees/pipeline-v2/.git
gitdir: /workspace/solution/repo/.git/worktrees/data-pipeline
```

So the back-reference (worktree → main repo) was fine; only the forward reference
(main repo → worktree) was broken, which is exactly what `git worktree repair` fixes.

## Steps and commands run

All commands were run from the main worktree, `/workspace/solution/repo`.

1. Reproduce the broken state:

   ```bash
   bash inputs/setup.sh
   ```

2. Inspect the broken registration:

   ```bash
   cd /workspace/solution/repo
   git worktree list
   git worktree list --porcelain
   cat .git/worktrees/data-pipeline/gitdir
   ```

3. Repair the registration, pointing Git at the worktree's current location:

   ```bash
   git worktree repair .worktrees/pipeline-v2
   ```

   Output:

   ```
   repair: gitdir incorrect: /workspace/solution/repo/.git/worktrees/data-pipeline/gitdir
   ```

   Git rewrote the stale pointer to the checkout's actual path:

   ```
   $ cat /workspace/solution/repo/.git/worktrees/data-pipeline/gitdir
   /workspace/solution/repo/.worktrees/pipeline-v2/.git
   ```

## After the fix — what Git reports

`git worktree list`:

```
/workspace/solution/repo                        12629ff [master]
/workspace/solution/repo/.worktrees/pipeline-v2 a4f5b32 [feature/data-pipeline]
```

`git worktree list --porcelain`:

```
worktree /workspace/solution/repo
HEAD 12629ffc1030db8306cdcc25ec4ac7e593d089e5
branch refs/heads/master

worktree /workspace/solution/repo/.worktrees/pipeline-v2
HEAD a4f5b320e97aaedb0207e06f62cb91c9685ae3ae
branch refs/heads/feature/data-pipeline
```

`git branch -vv`:

```
+ feature/data-pipeline a4f5b32 (/workspace/solution/repo/.worktrees/pipeline-v2) WIP: data ingestion stub
* master                12629ff Initial commit
```

The `prunable` marker is gone, and the feature branch is now attributed to the correct
checkout path.

## Confirmation

The feature branch checkout is properly registered and at the expected location:

- `git worktree list` shows the linked worktree at
  `/workspace/solution/repo/.worktrees/pipeline-v2` on branch `feature/data-pipeline`
  at commit `a4f5b32` ("WIP: data ingestion stub"), with no `prunable` status.
- Running `git status` inside `/workspace/solution/repo/.worktrees/pipeline-v2` reports
  `On branch feature/data-pipeline` / `nothing to commit, working tree clean`.
- `git rev-parse --show-toplevel` there resolves to
  `/workspace/solution/repo/.worktrees/pipeline-v2`, and `git rev-parse --git-dir`
  resolves to `/workspace/solution/repo/.git/worktrees/data-pipeline`.
- The feature branch's work is intact — `src/pipeline.py` contains both the original
  `process_batch` stub and the added `ingest` stub, and the branch history
  (`12629ff Initial commit` → `a4f5b32 WIP: data ingestion stub`) is preserved.

The relocated worktree is fully functional and correctly tracked by Git again.
