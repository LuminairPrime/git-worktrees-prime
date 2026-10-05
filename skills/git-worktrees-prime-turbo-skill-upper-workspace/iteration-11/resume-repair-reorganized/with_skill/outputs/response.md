Resume in `case03/checkouts/adapter-current` on `task/adapter`, no new checkout, no integration:

1. Confirm current location and registration:
```sh
pwd
realpath case03/checkouts/adapter-current
git worktree list --porcelain -z
```

2. Reconnect relocated checkout from `adapter-old`, then verify — do not prune:
```sh
git worktree repair "$(realpath case03/checkouts/adapter-current)"
git worktree list --porcelain -z
```

3. Establish starting state in same checkout:
```sh
git -C case03/checkouts/adapter-current branch --show-current
git -C case03/checkouts/adapter-current status --short --branch --untracked-files=all
git -C case03/checkouts/adapter-current rev-parse HEAD
git -C case03/checkouts/adapter-current log --oneline -5
# check for in-progress merge/rebase/bisect before editing; stop if present
git -C case03/checkouts/adapter-current status
ls case03/checkouts/adapter-current/.git/MERGE_HEAD case03/checkouts/adapter-current/.git/CHERRY_PICK_HEAD case03/checkouts/adapter-current/.git/REBASE_HEAD 2>&1 || true
```

4. Consume completed schema worker result:
```sh
cat worker-status.json
git branch --contains schema/prep -a || true
git log --oneline -3 schema/prep
cat case03/checkouts/adapter-current/SCHEMA_VERSION
```

5. Inspect current `encode_record` and draft notes without changing notes:
```sh
grep -rn "def encode_record" case03/checkouts/adapter-current
cat existing-draft-notes-file
git -C case03/checkouts/adapter-current diff -- case03/checkouts/adapter-current
```

6. Finish `encode_record` only:
- `name.strip().lower()`
- `enabled` as `bool`
- `schema` from `SCHEMA_VERSION`
- keep draft notes untouched.

7. Validate with project check from task checkout:
```sh
git -C case03/checkouts/adapter-current status --short --branch
./project-check-from-repo-docs
```

8. Commit on `task/adapter`:
```sh
git -C case03/checkouts/adapter-current add -p
git -C case03/checkouts/adapter-current commit -m "Finish encode_record"
git -C case03/checkouts/adapter-current rev-parse HEAD
git -C case03/checkouts/adapter-current status --short --branch
```

9. Leave ready for review, no integration/publishing:
```sh
git worktree list --porcelain -z
git -C case03/checkouts/adapter-current branch --show-current
```
Retained: checkout `case03/checkouts/adapter-current` on `task/adapter` + tip commit. Not merged, not pushed, not removed, branch not deleted, no prune.

