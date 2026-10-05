No — don't remove it yet. A detached HEAD has no branch pointing at your three commits. Deleting the worktree (or letting the directory go) orphans them, and they'll be garbage-collected once the reflog expires. Anchor them to a durable ref first, then remove the checkout.

Run these in order, substituting `<repo>` (any surviving checkout or the bare repo) and `<worktree>` (the disposable checkout's absolute path):

**1. Confirm ownership and identity of the checkout**

```sh
git -C "<repo>" worktree list --porcelain -z
```

Verify the exact absolute path, that it's registered, and note its branch/HEAD line.

**2. Check what state would disappear with the directory**

```sh
git -C "<worktree>" status --short --branch --untracked-files=all
git -C "<worktree>" status --short --ignored
git -C "<worktree>" rev-parse HEAD
git -C "<worktree>" log --oneline -5
```

Uncommitted tracked edits, untracked files, ignored files, or an unfinished operation (rebase/merge in progress) must be committed, moved, or deliberately discarded *before* removal — a clean status does not cover ignored files or detached commits.

**3. Anchor the detached commits**

Either point a new branch at the detached tip:

```sh
git -C "<repo>" branch "<task-branch>" "<detached-tip-sha>"
```

…or, if the work is already integrated elsewhere, verify that first:

```sh
git -C "<repo>" merge-base --is-ancestor "<detached-tip-sha>" "<integration-ref>"
```

Exit 0 means the tip is already contained in the integration target, so a branch is optional. Otherwise prefer actually merging/cherry-picking the three commits into the target branch, then verify.

**4. Remove the checkout (only after steps 2–3)**

```sh
git -C "<repo>" worktree remove "<worktree>"
```

If step 2 shows leftover uncommitted state, this refuses without `--force`; resolve that state rather than forcing.

**5. Clean up metadata and verify**

```sh
git -C "<repo>" worktree list --porcelain -z
git -C "<repo>" worktree prune --dry-run --verbose
```

Review every dry-run entry — prune only intentionally removed worktrees:

```sh
git -C "<repo>" worktree prune --verbose
```

**6. Branch deletion (separate decision)**

Only delete `<task-branch>` once its work is verified integrated into the intended target:

```sh
git -C "<repo>" branch -d "<task-branch>"
```

If `-d` refuses, retain the branch until you've confirmed it's obsolete — `-D` discards unverified history and needs your explicit authorization.

Report what survives: the branch/PR/integration ref carrying the three commits, and confirmation the worktree path and its registration are gone. Pruning does not delete branches, and it must never be used to hide a missing-but-offline checkout.
