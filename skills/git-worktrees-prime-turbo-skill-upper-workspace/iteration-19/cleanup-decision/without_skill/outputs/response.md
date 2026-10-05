In this environment `/repo` does not exist, so I can't execute this - walkthrough for your repo:

Assumes main checkout at `/repo`, task checkout at `/repo/.worktrees/old-task`.

1. Don't run from inside the worktree to delete:
```bash
pwd
git rev-parse --show-toplevel
git worktree list -v
```

2. Check task worktree is clean:
```bash
git -C /repo/.worktrees/old-task status --short --branch
git -C /repo/.worktrees/old-task stash list
git -C /repo/.worktrees/old-task log --branches --not --remotes --oneline
```
Must be empty / no ahead commits you need. If dirty, stop.

3. Identify branch:
```bash
git -C /repo/.worktrees/old-task rev-parse --abbrev-ref HEAD
# e.g. TASK-BRANCH
```

4. Check merge - squash caveat:
```bash
git -C /repo branch --merged main | grep TASK-BRANCH
git -C /repo cherry main TASK-BRANCH
```
After squash-merge this will still show as **not merged** - squash creates a new SHA with no shared ancestry. Do not rely on `-d`. Verify externally instead:
```bash
gh pr view TASK-BRANCH --state merged --json state,mergedAt,mergeCommit
git -C /repo log --oneline main -n 20
```

Only proceed if PR state is `MERGED`.

5. Remove checkout:
```bash
git -C /repo worktree remove /repo/.worktrees/old-task
```
Use `--force` only if step 2 was clean but it still refuses (e.g. locked submodules). Never `--force` a dirty tree.

6. Delete branch - `-D` required after squash:
```bash
git -C /repo branch -D TASK-BRANCH
```
`-d` will fail by design here.

7. Prune and verify:
```bash
git -C /repo worktree prune -v
git worktree list -v
git -C /repo branch --list 'TASK-BRANCH'
git -C /repo status --short --branch
```

