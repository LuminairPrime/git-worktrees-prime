In `case03/checkouts/adapter-current` - reuse, do not re-create:

1. Confirm current inventory - relocated checkout will show stale:
```bash
git worktree list --porcelain -z | tr '\0' '\n'
```

2. Repair relocated registration from `adapter-old` -> `adapter-current` using current absolute path, from primary repo:
```bash
git -C "<primary-root>" worktree repair "<absolute-path>/case03/checkouts/adapter-current"
```

3. Verify repair, do not prune live registration:
```bash
git worktree list --porcelain -z | tr '\0' '\n'
```

4. Lock to task checkout, verify branch `task/adapter` and starting state:
```bash
cd "<absolute-path>/case03/checkouts/adapter-current"
pwd
git rev-parse --show-toplevel
git branch --show-current
git status --short --branch
git log --oneline -5
git rev-parse HEAD
```

5. Check no ongoing operation / other owner, keep draft notes - do not reset/clean:
```bash
git status --short
ls .git/MERGE_HEAD .git/REBASE_HEAD .git/CHERRY_PICK_HEAD .git/BISECT_LOG 2>&1
git stash list
```

6. Consume completed schema worker result:
```bash
cat worker-status.json
git log --oneline -3 schema/prep
git show schema/prep:SCHEMA_VERSION 2>/dev/null || grep -R "SCHEMA_VERSION" -n .
```

7. In this same checkout, finish `encode_record` only:
   - `name.strip().lower()`
   - `enabled` as `bool`
   - `schema` from `SCHEMA_VERSION`
   - Keep existing draft notes, no bulk copy from other checkout.

8. Validate with project check from task checkout:
```bash
cat README* CONTRIBUTING* 2>/dev/null | grep -i -A2 check
./project-check || make check || pytest -q || npm test
```

9. Commit on `task/adapter` in this checkout:
```bash
git branch --show-current
git add -p
git status --short
git commit -m "adapter: finish encode_record"
git log --oneline -3
```

10. Leave ready for review - no integration/publishing:
```bash
git status --short --branch
git worktree list --porcelain -z | tr '\0' '\n'
```
Do not: merge/rebase to target, push, open PR, `worktree remove/move/prune`, `branch -d/-D`.
Report: `case03/checkouts/adapter-current`, branch `task/adapter`, HEAD commit, check output, retained for review.

