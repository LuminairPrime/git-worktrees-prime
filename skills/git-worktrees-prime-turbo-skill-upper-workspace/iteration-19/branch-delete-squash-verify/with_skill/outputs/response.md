No — `git branch -D task/export` now would bypass the safeguard without proof. `git branch -d` failing is expected after squash-merge: squash breaks ancestry.

Run in order, from a surviving checkout:

1. Confirm checkout already gone, branch still exists:
```sh
git worktree list --porcelain -z
git branch --list "task/export"
git rev-parse --verify "refs/heads/task/export^{commit}"
```

2. Get current integration ref:
```sh
git fetch origin
git rev-parse --verify "main^{commit}"
git rev-parse --verify "origin/main^{commit}"
```

3. Document why `-d` refuses — exit non-zero expected for squash:
```sh
git merge-base --is-ancestor "task/export" "main"; echo $?
```
`branch -d` checks ancestry, not content. Success would not prove integration either.

4. Verify squash content — replacement commit + no unique changes left on branch:
```sh
git log --oneline main --grep="task/export"
git log --oneline main --grep="export"
git cherry main task/export
git log --cherry-pick --right-only --oneline main...task/export
git diff main...task/export
```
Integrated = `cherry` shows only `-`, `log --cherry-pick --right-only` empty, `diff main...task/export` empty.

5. `-D` acceptable only if all true:
* branch is task-owned, not checked out elsewhere, not needed for pending review
* work verified integrated into intended `main` per step 4 (closed PR alone insufficient), or preserved under another durable ref, or explicitly authorized to abandon
* obsolete squash history authorized to discard

Then:
```sh
git branch -D task/export
git branch --list "task/export"
git worktree list --porcelain -z
```
