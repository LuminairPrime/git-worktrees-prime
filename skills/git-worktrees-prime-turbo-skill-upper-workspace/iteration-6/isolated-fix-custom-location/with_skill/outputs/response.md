Exact sequence I would run, in order, without touching the colleague checkout state:

1. Confirm current checkout and preserve state:
```sh
pwd
git rev-parse --show-toplevel
git branch --show-current
git status --short --branch --untracked-files=all
git worktree list --porcelain
```
Check: unrelated modified notes + untracked draft present; no `MERGE_HEAD`/`REBASE`/`CHERRY_PICK` in progress. Do not `stash/reset/clean/checkout/pull` here.

2. Resolve requested base without pulling into this checkout:
```sh
git fetch origin release/next
git rev-parse --verify --show-short release/next
```

3. Verify `project/scratch-checkouts/normalize/` ignore coverage from primary root:
```sh
git rev-parse --path-format=absolute --git-path info/exclude
git check-ignore -q project/scratch-checkouts/normalize/
```
Require exit `0`. If not ignored, add that relative path to `info/exclude`, do not edit tracked `.gitignore` for this.

4. Create separate checkout:
```sh
git worktree add -b task/normalize project/scratch-checkouts/normalize release/next
```
Use `-b`, not `-B`; do not transfer uncommitted/untracked files.

5. Verify creation:
```sh
git worktree list --porcelain -z
git -C project/scratch-checkouts/normalize rev-parse --abbrev-ref HEAD
git -C project/scratch-checkouts/normalize log --oneline -1
git -C project/scratch-checkouts/normalize status --short --branch
git check-ignore -q project/scratch-checkouts/normalize/
```

6. In `project/scratch-checkouts/normalize` only: fix `normalize_label` to `strip()` surrounding whitespace then `lowercase`, run project documented `check/test` from that path, review diff:
```sh
git -C project/scratch-checkouts/normalize status --short --branch
# edit only task file(s)
# run project's check from task checkout, e.g. per README/CONTRIBUTING
git -C project/scratch-checkouts/normalize diff
```

7. Commit on task branch:
```sh
git -C project/scratch-checkouts/normalize add <task-file(s)>
git -C project/scratch-checkouts/normalize commit -m "Fix normalize_label to strip and lowercase"
git -C project/scratch-checkouts/normalize status --short --branch
git -C project/scratch-checkouts/normalize log --oneline -2
git -C project/scratch-checkouts/normalize branch --show-current
```

8. Leave ready for review, no integrate/publish:
```sh
git worktree list --porcelain
git status --short --branch --untracked-files=all
```
Check: primary still on original branch with same notes/draft intact; task checkout at `project/scratch-checkouts/normalize` on `task/normalize` from `release/next`, clean, check passed. No merge, rebase into target, push, worktree remove, or branch delete.

