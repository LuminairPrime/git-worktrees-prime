No — don't `-D` yet. `-d` fails by design for squash-merges: no commit from `task/export` is an ancestor of `main`, so `git` can't prove integration.

Verify content integration first, then `-D` is expected:

1. Sync and inspect state:
```bash
git fetch origin
git branch -vv --list task/export main
git status --short --branch
git log --oneline task/export -n 10
```

2. Update `main` and find squash commit:
```bash
git checkout main
git pull --ff-only
git log --oneline -n 15
git log --oneline --grep=export -n 5
git branch --merged main --list task/export
# expected: no output; confirms why `-d` refuses
```

3. Verify no unique content remains. Empty output = fully integrated:
```bash
git diff main...task/export --stat
git diff main...task/export
git cherry main task/export
# expected `cherry`: all lines prefixed with `-`, none with `+`
```

If diff is non-empty, stop: that is unmerged work. Inspect it, cherry-pick/port or merge it, then repeat step 3.

4. Delete only when step 3 is empty and squash commit exists in `origin/main`:
```bash
git branch -D task/export
git push origin --delete task/export # only if remote branch exists
git fetch -p
```

