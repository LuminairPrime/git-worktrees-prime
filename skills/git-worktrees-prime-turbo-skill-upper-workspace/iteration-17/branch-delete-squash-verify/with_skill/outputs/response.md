No. Do not run `git branch -D task/export` yet. `branch -d` refusal is expected after squash-merge.

Squash integration breaks ancestry: `task/export` tip is not an ancestor of `main`, so `merge-base --is-ancestor` fails and `-d` refuses. `-d` may also check upstream, not `main` — neither success nor failure proves integration.

Verify in this order from a surviving checkout:

1. Confirm checkout is gone and branch is not checked out elsewhere:
```sh
git worktree list --porcelain -z
git branch --list "task/export"
git rev-parse --verify "refs/heads/task/export^{commit}"
```

2. Resolve current integration ref:
```sh
git fetch origin main
git rev-parse --verify "main^{commit}"
git rev-parse --verify "refs/heads/task/export^{commit}"
```

3. Confirm ancestry break — expect non-zero exit:
```sh
git merge-base --is-ancestor "task/export" "main"; echo $?
```

4. Verify replacement squash commit and that no unique changes remain:
```sh
git log --oneline -10 main
git cherry main "task/export"
git diff main..."task/export" --stat
```
`cherry` should show `-` for all task commits, `log` should show the squash commit, `diff` should show no valuable unique patch. A closed PR alone is insufficient.

`-D` is acceptable only when all hold:

* branch is task-owned, unused, not checked out elsewhere
* work is verified integrated in `main` per step 4, preserved under another durable ref, or explicitly authorized for abandonment
* no pending review needs the branch

Then:
```sh
git branch -D task/export
git branch --list "task/export"
git worktree list --porcelain -z
```

