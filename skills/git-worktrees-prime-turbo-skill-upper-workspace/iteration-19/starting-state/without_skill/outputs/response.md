Cannot determine base from current workspace: `/tmp/skill-up-2522527903` is empty and not a git repo.

Do not assume `main` is integration target. Determine it per-repo:

1. Find default/integration branch:
```bash
git remote show origin | grep "HEAD branch"
git symbolic-ref refs/remotes/origin/HEAD
gh repo view --json defaultBranchRef --jq .defaultBranchRef.name
```
Common targets are `main`, `master`, `develop`, or `trunk` - use what the repo declares.

2. Base for feature X:
```bash
git fetch origin
git worktree add ../feature-X -b feature/X origin/<default-branch>
```
Base off fresh `origin/<default-branch>`, not local stale branch.

3. Task branch vs disposable checkout:
- Task branch: named persistent branch (`-b feature/X`), do work/commits there, push for review, keep until merged.
- Disposable inspection: detached, no new branch, delete after:
```bash
git worktree add --detach /tmp/opencode/inspect-X origin/<default-branch>
git worktree remove --force /tmp/opencode/inspect-X
```

Provide repo path/URL and desired default branch if you want me to create the worktree.
