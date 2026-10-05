No — do not remove it yet. Detached `HEAD` commits have no ref. Removing the checkout leaves them dangling until `gc` deletes them.

Run in order, from main repo:

1. Check worktrees:
```bash
git worktree list -v
```

2. Check disposable checkout is detached + what will be lost:
```bash
git -C <disposable-path> status --short --branch
git -C <disposable-path> branch --show-current
git -C <disposable-path> log --oneline --decorate -5
git -C <disposable-path> rev-parse HEAD
```

`branch --show-current` empty = detached, as expected.

3. Preserve all 3 commits with a ref first:
```bash
git -C <disposable-path> branch rescue/<name> HEAD
```

Use `tag <name> HEAD` if you want immutable instead.

4. Verify rescue from main repo:
```bash
git branch -vv --contains <HEAD-sha-from-step-2>
git log --oneline --decorate rescue/<name> -3
```

Must show 3 commits on `rescue/<name>`.

5. Only then remove checkout:
```bash
git worktree remove <disposable-path>
git worktree list
git worktree prune -v
```

Use `--force` only if step 2 showed dirty/locked state you intentionally discard. If dirty and valuable: commit or `git -C <disposable-path> stash -u` before step 3.

After that `rescue/<name>` survives in main repo for merge/cherry-pick/push.

