Do not run `-D` yet. This is expected: `git branch -d` checks ancestry, squash-merge creates a new commit on `main`, so `task/export` is never reported as merged.

Verify semantic integration first, then `-D` is acceptable.

Run in order:

1. Update refs:
```bash
git fetch origin --prune
git switch main
git pull --ff-only
```

2. Confirm squash commit exists on `main`:
```bash
git log --oneline --graph --decorate -15 main
git log --merges --oneline -10 main
git log --oneline main --grep="task/export\|export\|#[0-9]" -10
```

3. List commits unique to task branch:
```bash
git log --oneline main..task/export
git branch --merged main | grep task/export || echo "not ancestry-merged, expected for squash"
```

4. Check patch-equivalence, this is the key check:
```bash
git cherry main task/export
git diff main...task/export
```
Accept only if: `git cherry` shows `-` for every commit (already equivalent upstream), and `git diff main...task/export` is empty or only trivial/expected conflicts resolved during squash.

If a `+` line remains, inspect it:
```bash
git show <commit>
git log -p main --grep="<subject>" -1
```

5. Confirm no checkout / work left:
```bash
git worktree list
git status --short --branch
git branch -a | grep export
```

6. Delete only after 2-5 pass, `main` is pushed and CI green, and no unique work remains:
```bash
git branch -D task/export
git push origin --delete task/export
```

Optional safety if unsure:
```bash
git branch backup/task/export task/export
```

`-D` is acceptable when: content, not commits, is verified in up-to-date `main`, `cherry`/`diff` prove nothing unique is lost, and you accept losing the original commit granularity.
