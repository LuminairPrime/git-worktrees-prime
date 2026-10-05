Do not run `git branch -D task/export` yet. `git branch -d` refusal is expected after squash-merge.

`branch -d` checks upstream ancestry, not your integration target. Squash breaks ancestry, so `-d` fails even when integration succeeded. `-D` is only acceptable after you verify integration + ownership.

Run in order from a surviving checkout:

1. Confirm checkout is gone and branch is not checked out elsewhere:
```sh
git worktree list --porcelain -z
git branch --list task/export
git rev-parse --verify refs/heads/task/export^{commit}
```

2. Get verified current integration ref:
```sh
git fetch origin main
git rev-parse --verify refs/heads/main^{commit}
git rev-parse --verify refs/remotes/origin/main^{commit}
git log --oneline -5 task/export
git log --oneline -5 main
```

3. Ancestry check - exit 0 = ancestor, non-zero needs review:
```sh
git merge-base --is-ancestor task/export main; echo $?
```
Expect failure for squash. That alone is not authorization for `-D`.

4. Squash-specific verification - verify replacement commits and resulting changes:
```sh
git log --oneline main --grep=export -10
git cherry main task/export
git diff main...task/export
```
`cherry` should show all `-` (applied), `diff main...task/export` should be empty / only intended leftovers. If non-empty, work is not fully integrated - retain branch.

5. Delete only if all true:
* branch is task-owned, unused, no pending review
* work verified integrated above, or preserved under another ref, or explicitly authorized to abandon
* closed PR alone is insufficient

Then:
```sh
git branch -D task/export
git worktree list --porcelain -z
git branch --list task/export
```

