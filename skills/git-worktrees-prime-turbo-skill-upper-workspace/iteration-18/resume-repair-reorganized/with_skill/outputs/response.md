In `case03/checkouts/adapter-current`, in order:

1. Reuse same checkout, fix registration:
```sh
cd case03/checkouts/adapter-current
pwd
git worktree list
git worktree list --porcelain -z
```
Stale entry still points at `adapter-old`.

2. Repair moved checkout, do not move by filesystem, do not prune live entry:
```sh
git -C "<primary-root>" worktree repair "<abs-path>/case03/checkouts/adapter-current"
git worktree list
git worktree list --porcelain -z
```
Verify new path registered.

3. Confirm task state:
```sh
git branch --show-current # expect task/adapter
git status
git log --oneline -3
test ! -e .git/MERGE_HEAD -a ! -e .git/REBASE_HEAD -a ! -e .git/CHERRY_PICK_HEAD
git worktree list # task/adapter only here
```

4. Use schema result read-only, no checkout switch, no integration:
```sh
cat worker-status.json # schema worker complete on schema/prep
git log --oneline -3 schema/prep
git show schema/prep --stat
git show schema/prep:SCHEMA_VERSION-source
```

5. Finish `encode_record` in place, keep existing draft notes:
- `name.strip().lower()`
- `enabled` as boolean
- `schema` from `SCHEMA_VERSION`

Check:
```sh
git diff
```

6. Validate, commit on same branch:
```sh
# run project check
git status
git add <edited-adapter-file>
git branch --show-current
git commit -m "Finish encode_record"
git log --oneline -3
git status
```

7. Leave ready for review:
```sh
git worktree list
git branch --show-current
git status
```
Retain checkout and `task/adapter`. No `remove`, `branch -d/-D`, `prune`, `merge/rebase`, `push`/publish.

