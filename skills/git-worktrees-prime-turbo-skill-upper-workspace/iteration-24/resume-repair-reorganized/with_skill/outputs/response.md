In `case03/checkouts/adapter-current`, in order:

1. Repair registration first - do not prune/move/delete/recreate:
```sh
git -C <primary-root> worktree list --porcelain -z
git -C <primary-root> worktree repair "$PWD/case03/checkouts/adapter-current"
git -C <primary-root> worktree list --porcelain -z
```

2. Reuse same checkout, verify path/branch/state:
```sh
cd case03/checkouts/adapter-current
pwd
git rev-parse --show-toplevel
git branch --show-current # expect task/adapter
git status --short --branch --untracked-files=all
git log --oneline -3
# check no MERGE_HEAD/REBASE_HEAD/CHERRY_PICK_HEAD in $(git rev-parse --git-path MERGE_HEAD) etc.
```

3. Use completed schema worker result:
```sh
cat worker-status.json # verify schema/prep complete
grep -rn "encode_record\|SCHEMA_VERSION" -- .
```

4. Finish `encode_record` in place, keep draft notes - no reset/clean:
- `name.strip().lower()`
- `enabled` as `bool`
- `schema` from `SCHEMA_VERSION`

5. Verify diff preserves draft notes:
```sh
git diff --stat
git diff
```

6. Validate with project check, must pass:
```sh
make check # or repo-documented check
```

7. Commit on `task/adapter` in this checkout:
```sh
git branch --show-current
git add <adapter-file>
git status --short --branch
git commit -m "Finish encode_record"
git log --oneline -2
git status --short --branch
git worktree list --porcelain -z
```

Leave `case03/checkouts/adapter-current` on `task/adapter` ready for review. No merge/rebase/push, no `worktree remove/move/prune`, no `branch -d`.

