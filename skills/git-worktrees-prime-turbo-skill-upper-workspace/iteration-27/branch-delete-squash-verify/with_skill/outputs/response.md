No - do not run `git branch -D task/export` yet. `branch -d` refusal is expected after squash-merge.

Squash breaks ancestry, `branch -d` checks ancestry not patch-equivalence. Closed PR is not evidence.

Run in order from a surviving checkout:

1. Confirm checkout is gone and branch is unused:
```sh
git worktree list --porcelain -z
git branch --show-current
git status --short --branch --untracked-files=all
```

2. Get current integration ref:
```sh
git fetch origin
git rev-parse --verify "task/export^{commit}"
git rev-parse --verify "main^{commit}"
git rev-parse --verify "origin/main^{commit}"
```

3. Confirm ancestry failure is squash-related:
```sh
git merge-base --is-ancestor task/export main; echo $?
```
`1` expected - explains `branch -d` refusal, not data loss.

4. Verify replacement squash commit and resulting changes:
```sh
git log --oneline main -n 10
git cherry main task/export
git merge-base main task/export
```
`git cherry` must show `-` for every task commit, no `+`. `log` must show the squash commit. Then compare effects:
```sh
git show --stat <squash-sha>
git diff <base-sha> task/export --stat
git diff task/export main --stat
```
Remaining `task/export` vs `main` diff must be only unrelated `main` progress, no missing task work.

`-D` is acceptable only when all true:

* branch is task-owned, not checked out, not needed for pending review
* work verified integrated above into intended target `main`, or preserved under another durable ref, or explicitly authorized for abandonment

Then only:
```sh
git branch -D task/export
git branch --list "task/export"
git worktree list --porcelain -z
```
