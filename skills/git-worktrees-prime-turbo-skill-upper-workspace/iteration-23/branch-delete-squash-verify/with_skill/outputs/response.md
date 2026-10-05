No — do not run `-D` yet. `branch -d` refusal after squash-merge is expected, not proof of loss.

Squash creates new commit(s), so ancestry is broken:

1. Confirm branch still exists and where you are running from (checkout already removed, use surviving checkout):
```sh
git worktree list --porcelain -z
git branch --list "task/export"
git rev-parse --verify "refs/heads/task/export^{commit}"
```

2. Get current integration ref — `branch -d` may check upstream, not `main`:
```sh
git fetch origin
git rev-parse --verify "refs/heads/main^{commit}"
git rev-parse --verify "refs/remotes/origin/main^{commit}"
```

3. Prove ancestry break (expect exit `1`):
```sh
git merge-base --is-ancestor "task/export" "main"; echo $?
```

4. Verify content integration — replacement squash commit, not ancestry:
```sh
git log --oneline -n 10 main
git cherry main "task/export"
git diff "main...task/export"
```
Integrated iff: `cherry` shows only `-` (all upstreamed), triple-dot `diff` is empty except post-squash `main` advances. Find squash commit with `log` and `show` it if ambiguous.

5. `branch -D` only when all true:
* diff/cherry verification above passed
* branch is task-owned, not checked out elsewhere, no pending review — closed PR alone is insufficient
* work is in `main` or preserved under another durable ref, or abandonment explicitly authorized

Then, in order:
```sh
git branch -D "task/export"
git branch --list "task/export"
git worktree list --porcelain -z
git worktree prune --dry-run --verbose
```

