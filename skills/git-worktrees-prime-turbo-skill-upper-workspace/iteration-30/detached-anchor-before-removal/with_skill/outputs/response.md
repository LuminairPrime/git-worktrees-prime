No — do not `rm -rf` it.

Removal deletes that checkout's `HEAD`/index. Detached commits with no ref become unreachable and subject to GC. Anchor them first.

Order I would run, with `<worktree>` = exact linked path, `<primary-root>` = main checkout, `<preserve-branch>` = new durable ref:

1. Confirm inventory and ownership:
```bash
git worktree list --porcelain
```

2. Confirm target is linked, detached, and identify tip:
```bash
git -C "<worktree>" rev-parse --show-toplevel
git -C "<worktree>" branch --show-current
git -C "<worktree>" rev-parse HEAD
git -C "<worktree>" log --oneline --decorate -5
git -C "<worktree>" status --porcelain=v1 -uall
```

Expected: `branch --show-current` empty/detached, `log` shows your 3 valuable commits at `HEAD`.

3. Check for lossy state:
```bash
git -C "<worktree>" stash list
test -f "<worktree>/.git/MERGE_HEAD" -o -f "<worktree>/.git/CHERRY_PICK_HEAD" -o -f "<worktree>/.git/REBASE_HEAD" && echo "unfinished operation"
```

4. Preserve detached tip outside deletion path — this keeps all 3 if linear:
```bash
git -C "<worktree>" branch "<preserve-branch>" HEAD
git -C "<worktree>" log --oneline --decorate -3 "<preserve-branch>"
git -C "<worktree>" branch --contains HEAD --list "<preserve-branch>"
```

5. Leave checkout, stop task processes using it:
```bash
cd "<primary-root>"
```

6. Remove through Git only:
```bash
git -C "<primary-root>" worktree remove "<worktree>"
```

Do not add `--force` to bypass dirty/untracked check without authorization. Do not `git worktree prune` — that only cleans stale metadata.

7. Verify:
```bash
git worktree list --porcelain
test ! -e "<worktree>" && echo "path gone"
git branch --list "<preserve-branch>"
git log --oneline --decorate -3 "<preserve-branch>"
```

Retain `<preserve-branch>` — checkout removal leaves branches. Delete it only after verified integration elsewhere.

