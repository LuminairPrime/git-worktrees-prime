Exact sequence, in order. Assumes starting `pwd` is `project/` colleague checkout:

1. Inventory, prove colleague checkout untouched — read-only:
```sh
pwd
git rev-parse --show-toplevel
git worktree list --porcelain
git status --short --branch
git rev-parse --verify "release/next^{commit}"
```

2. Verify destination is ignored before creation — require exit `0`:
```sh
git check-ignore -q -- "scratch-checkouts/normalize/"
echo $?
```

> If non-zero: stop and add `scratch-checkouts/` to `$(git rev-parse --path-format=absolute --git-path info/exclude)` in primary, do not modify tracked `.gitignore` in colleague checkout. Re-run check.

3. Refresh base without touching colleague checkout:
```sh
git fetch origin release/next
git rev-parse --verify "release/next^{commit}"
```

4. Create separate checkout, new branch from base:
```sh
git worktree add -b task/normalize scratch-checkouts/normalize release/next
```

Do not use `-B`, `stash`, `reset`, `clean`, `pull`, or `checkout` in `project/`.

5. Verify new checkout:
```sh
git -C scratch-checkouts/normalize rev-parse --show-toplevel
git -C scratch-checkouts/normalize status --short --branch
git -C scratch-checkouts/normalize rev-parse HEAD
git -C scratch-checkouts/normalize log --oneline -1
git worktree list --porcelain
git check-ignore -q -- "scratch-checkouts/normalize/"
```

6. Fix only in `scratch-checkouts/normalize`:
```sh
grep -rn "def normalize_label\|function normalize_label\|normalize_label" scratch-checkouts/normalize
```

Edit that definition to:
```py
return label.strip().lower()
```

7. Run project's documented check from task checkout:
```sh
cd scratch-checkouts/normalize
# inspect README/CONTRIBUTING/pyproject.toml/package.json/Makefile for `check` command, then e.g.:
# pytest / npm test / npm run check / make check
```

8. Commit on `task/normalize`:
```sh
git -C scratch-checkouts/normalize status --short --branch
git -C scratch-checkouts/normalize diff
git -C scratch-checkouts/normalize add <file-containing-normalize_label>
git -C scratch-checkouts/normalize commit -m "Fix normalize_label to strip and lowercase"
git -C scratch-checkouts/normalize log --oneline -2
git -C scratch-checkouts/normalize status --short --branch
```

9. Leave ready, no integration:
```sh
git worktree list --porcelain
git status --short --branch
```

Retained: `project/scratch-checkouts/normalize` on `task/normalize` ready for review. Original notes/draft intact. No merge, push, `worktree remove/prune`, or `branch -d`.

