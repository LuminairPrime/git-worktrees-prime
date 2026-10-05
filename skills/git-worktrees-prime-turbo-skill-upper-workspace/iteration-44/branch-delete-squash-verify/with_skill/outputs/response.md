**Short answer: don't run `-D` yet.** `-d` refusing is expected for a squash merge — it only tests *ancestry* (fully merged into `branch.<name>.merge`, or into `HEAD` if no upstream is set), and a squash creates a new commit that is not a descendant of your tip. The refusal tells you nothing about whether your *content* landed. (Conversely, `-d` succeeding isn't proof either — its upstream may be stale.) Verify the changes, not the ancestry.

Here are the checks I'd run, in order:

### 1. Record what you're about to make unreachable
```sh
git log -1 --format='%H %ci %an %s' task/export
git reflog show task/export --date=iso -10
```
Write the full SHA down. This is your recovery path after `-D`; the reflog alone is not something to rely on.

### 2. Confirm nothing still holds the branch
```sh
git worktree list --porcelain
```
No checkout (main, linked worktree, stale registration) may have `task/export` checked out. If a removed path is still listed, dry-run `git worktree prune --dry-run --verbose` and review each entry before pruning — a missing directory can be an offline volume, not a deleted one.

### 3. Get a current integration target
```sh
git fetch origin --prune
git rev-parse --verify origin/main    # use the real target name, don't assume "main"
```
Your local view may simply be behind; fetch before judging anything.

### 4. Run the ancestry check anyway (it disambiguates)
```sh
git merge-base --is-ancestor task/export origin/main; echo $?
```
Exit `0` → it was a real merge/rebase-forward; `-d` should now succeed (if it still refuses, the upstream config is the problem, not the merge). Exit `1` → squash/rebase broke ancestry; continue below.

### 5. Find the squash commit on the target
```sh
git log --oneline --decorate --no-merges -n 30 origin/main
git log origin/main --oneline --grep='task/export'
git log origin/main --oneline --grep='<PR number or ticket>'
git show --stat <candidate-squash-commit>
```
Compare that commit's diffstat and message against `git show --stat task/export`.

### 6. Test the patches, not the history
```sh
git cherry -v origin/main task/export
git log --left-right --cherry-pick --oneline origin/main...task/export
```
`git cherry` marks a commit `-` when an equivalent patch (same patch-id) exists upstream. For a 1-commit branch squash 1:1, you'll see `-`. For a multi-commit branch squashed into one, patch-ids won't match and everything shows `+` — that is *not* evidence of missing work. Fall back to a content check:

```sh
base=$(git merge-base origin/main task/export)
git diff --stat "$base" task/export
git diff "$base" task/export > /tmp/task-export.patch
git apply --reverse --check /tmp/task-export.patch   # run with the target checked out, tree clean
```
Exit 0 means every change on your branch is already present in the target. If it fails because later commits touched the same lines, inspect per-path instead:
```sh
git diff task/export origin/main -- <paths your branch touched>
```
and confirm the only differences are unrelated follow-up work.

### 7. Confirm nothing else references the tip
```sh
git for-each-ref --format='%(refname:short) %(objectname:short)' | grep -w "$(git rev-parse --short task/export)"
git branch -vv
```
No tag, backup branch, or other ref should point at that SHA, and no other branch should be relying on it.

### 8. Delete and verify
```sh
git branch -D task/export
git branch --list 'task/export'     # expect empty
git worktree list --porcelain
```
Don't `git push origin --delete task/export` unless deleting the remote branch is separately in scope — collaborators may still need it.

### When `-D` is acceptable
- The tip's changes are verified present on the intended integration target (step 5/6), **or** you have explicit authorization to abandon them. A closed/merged PR alone is not sufficient evidence.
- You've recorded the SHA from step 1 (and confirmed no unmerged local commits appeared in its reflog after the merge).
- No other ref, checkout, or pending review depends on the branch.
- You're deleting a task-owned branch, not one you don't own.

If step 5 turns up no squash commit and the reverse-apply fails, **stop and keep the branch** — `-D` would discard work. Recovery if you delete anyway: `git branch task/export <recorded-SHA>` (works while the reflog entry survives, typically 90 days), or `git fsck --lost-found`.
