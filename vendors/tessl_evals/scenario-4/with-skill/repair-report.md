# Worktree Registration Repair Report

## Summary

A linked worktree for the `feature/data-pipeline` branch was relocated with the
operating system's file manager (`mv`) instead of `git worktree move`, leaving
Git's administrative record pointing at the old path. The registration was
restored with `git worktree repair`, and the checkout is now correctly tracked at
its current location.

- **Repository (main worktree):** `/workspace/solution/repo`
- **Branch:** `feature/data-pipeline`
- **Old (stale) path:** `/workspace/solution/repo/.worktrees/data-pipeline`
- **New (current) path:** `/workspace/solution/repo/.worktrees/pipeline-v2`
- **Feature tip:** `7718ac76a1cbcf105dbb0fd1ef71588ab5df893e` ("WIP: data ingestion stub")

## 1. State before the fix

`git worktree list` reported the worktree at its **old** location and flagged it
as prunable:

```
$ git worktree list
/workspace/solution/repo                          c929303 [master]
/workspace/solution/repo/.worktrees/data-pipeline 7718ac7 [feature/data-pipeline] prunable
```

`git worktree list --porcelain` confirmed the reason:

```
worktree /workspace/solution/repo
HEAD c929303c11db6dcdf6b9660010dc14e60070adce
branch refs/heads/master

worktree /workspace/solution/repo/.worktrees/data-pipeline
HEAD 7718ac76a1cbcf105dbb0fd1ef71588ab5df893e
branch refs/heads/feature/data-pipeline
prunable gitdir file points to non-existent location
```

The physical directory no longer existed at that path — only
`.worktrees/pipeline-v2` existed on disk.

### Root cause

Git stores a linked worktree's registration in two mirrored pointer files:

1. **Admin side** — `.git/worktrees/data-pipeline/gitdir` contained the stale path:
   ```
   /workspace/solution/repo/.worktrees/data-pipeline/.git
   ```
2. **Checkout side** — `.worktrees/pipeline-v2/.git` contained the (still valid) back-pointer:
   ```
   gitdir: /workspace/solution/repo/.git/worktrees/data-pipeline
   ```

Because the checkout was moved with `mv`, the admin-side `gitdir` file was never
updated, so Git could not connect the registration to the live checkout.

## 2. Steps taken to restore the registration

The skill `git-worktrees-prime` prescribes, for a live checkout that was
relocated under raw Git:

> `git -C "<repo>" worktree repair "<worktree>"` using its current absolute path.
> Re-list worktrees to verify the new registration. Do not prune the live
> checkout's registration.

Run from the repository root, targeting the **current** absolute path of the
checkout:

```sh
$ git worktree repair /workspace/solution/repo/.worktrees/pipeline-v2
repair: gitdir incorrect: /workspace/solution/repo/.git/worktrees/data-pipeline/gitdir
```

Git rewrote the admin-side pointer file
`.git/worktrees/data-pipeline/gitdir` to the checkout's current location:

```
/workspace/solution/repo/.worktrees/pipeline-v2/.git
```

No `prune` was run — the registration was repaired, not removed, so the live
checkout and its branch were preserved.

## 3. State after the fix

`git worktree list` now reports the worktree at its correct current location, with
no `prunable` marker:

```
$ git worktree list
/workspace/solution/repo                        c929303 [master]
/workspace/solution/repo/.worktrees/pipeline-v2 7718ac7 [feature/data-pipeline]
```

`git worktree list --porcelain`:

```
worktree /workspace/solution/repo
HEAD c929303c11db6dcdf6b9660010dc14e60070adce
branch refs/heads/master

worktree /workspace/solution/repo/.worktrees/pipeline-v2
HEAD 7718ac76a1cbcf105dbb0fd1ef71588ab5df893e
branch refs/heads/feature/data-pipeline
```

`git branch -vv` now resolves the branch to the new path:

```
+ feature/data-pipeline 7718ac7 (/workspace/solution/repo/.worktrees/pipeline-v2) WIP: data ingestion stub
* master                c929303 Initial commit
```

## 4. Confirmation

- **Registration is correct:** `feature/data-pipeline` is registered at
  `/workspace/solution/repo/.worktrees/pipeline-v2` — the checkout's actual
  location — and the `prunable` flag is gone.
- **Expected location:** `git -C /workspace/solution/repo/.worktrees/pipeline-v2
  rev-parse --show-toplevel` resolves to that same path, and the worktree reports
  `## feature/data-pipeline` on the branch.
- **Work is intact:** the feature tip is still
  `7718ac76a1cbcf105dbb0fd1ef71588ab5df893e` ("WIP: data ingestion stub"), and the
  uncommitted-to-main work is present:

  ```
  $ cat .worktrees/pipeline-v2/src/pipeline.py
  def process_batch(items): pass
  def ingest(source, dest): pass
  ```

  ```
  $ git -C .worktrees/pipeline-v2 log --oneline
  7718ac7 WIP: data ingestion stub
  c929303 Initial commit
  ```

- **No data was lost:** the repair only rewrote Git's pointer metadata; no
  directory was moved, pruned, or deleted, and no branch was touched.
