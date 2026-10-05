No. Don't `-D` yet. `-d` refusal is expected after squash-merge.

Why: squash creates a new commit on `main`, it does not preserve `task/export` ancestry. `git branch -d` checks ancestry, so it fails even when fully integrated.

Verify first, in order:

1. Update refs:
```bash
git fetch origin
git switch main
git pull --ff-only
```

2. Confirm squash commit is on `origin/main`:
```bash
git log --oneline -10 origin/main
git log --oneline origin/main --grep="task/export"
git log --oneline origin/main --grep="export"
```
Find the single squash commit / PR number. `git merge-base --is-ancestor task/export main` will fail here - ignore it, it doesn't work for squash.

3. Confirm no unique changes remain on branch:
```bash
git diff main...task/export --stat
git diff main...task/export
```
Empty output = all `task/export` changes are in `main`. If non-empty, inspect it - do not delete.

Optional if using GitHub:
```bash
gh pr view task/export --state merged
gh pr list --head task/export --state merged
```

4. `-D` is acceptable only when:
* step 2 shows squash commit on `origin/main`, and
* step 3 diff is empty, and
* you have no unique commits to keep.

Then delete:
```bash
git branch -D task/export
git push origin --delete task/export
git fetch -p
```

