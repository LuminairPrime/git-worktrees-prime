Would run, in order, from the colleague's checkout — no in-place edits:

1. Confirm original is dirty and must stay intact:
```sh
git worktree list --porcelain -z
git status --short --branch
git rev-parse --verify "release/next^{commit}"
```

2. Confirm `task/normalize` is not already checked out elsewhere, and `project/scratch-checkouts/normalize` destination is ignored:
```sh
git check-ignore -q -- "project/scratch-checkouts/normalize/"
git fetch origin release/next
git rev-parse --verify "release/next^{commit}"
```

3. Create separate checkout, new branch from base — do not `pull`, `checkout`, `stash`, `reset`, or `clean` the original, do not copy notes/draft:
```sh
git worktree add -b "task/normalize" "project/scratch-checkouts/normalize" "release/next"
```

4. Verify new checkout:
```sh
git -C "project/scratch-checkouts/normalize" rev-parse --show-toplevel
git -C "project/scratch-checkouts/normalize" status --short --branch
git -C "project/scratch-checkouts/normalize" rev-parse HEAD
git check-ignore -q -- "project/scratch-checkouts/normalize/"
```

5. Fix only in `project/scratch-checkouts/normalize`: locate `def normalize_label`, change to `strip()` surrounding whitespace and `lower()`:
```sh
grep -rn "def normalize_label" "project/scratch-checkouts/normalize"
# edit that file to: return label.strip().lower()
```

6. Run project's check from new checkout per repo instructions:
```sh
git -C "project/scratch-checkouts/normalize" status --short --branch
# e.g. pytest / npm test / make check — run discovered check in that path
```

7. Commit on `task/normalize`, leave for review:
```sh
git -C "project/scratch-checkouts/normalize" diff
git -C "project/scratch-checkouts/normalize" add <fixed-file>
git -C "project/scratch-checkouts/normalize" commit -m "Fix normalize_label to strip whitespace and lowercase"
git -C "project/scratch-checkouts/normalize" status --short --branch
git -C "project/scratch-checkouts/normalize" log --oneline -1
git worktree list --porcelain -z
git status --short --branch
```

Retain: `project/scratch-checkouts/normalize` on `task/normalize` ready for review. Do not merge, push, `worktree remove`, `branch -d`, or `worktree prune`.

