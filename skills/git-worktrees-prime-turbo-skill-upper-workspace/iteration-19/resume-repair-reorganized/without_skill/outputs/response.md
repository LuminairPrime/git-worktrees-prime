In `case03/checkouts/adapter-current`, in order:

1. Move to current checkout and confirm reorg:
```sh
cd case03/checkouts/adapter-current
pwd
git rev-parse --show-toplevel
git branch --show-current
git status --short
```

2. Confirm on work branch, not detached:
```sh
git switch task/adapter
git branch --show-current
git log --oneline -3
```

3. Confirm schema worker done:
```sh
cat worker-status.json
# check: schema/prep == complete
grep -R "SCHEMA_VERSION" -n .
```

4. Inspect current stub:
```sh
grep -R "def encode_record" -n .
git status --short
# check: existing draft notes file present and unmodified
git diff --stat
```

5. Finish `encode_record` in place, keep draft notes untouched:
- `name = record["name"].strip().lower()`
- `enabled = bool(record["enabled"])`
- `schema = SCHEMA_VERSION`
- return dict with `name`, `enabled`, `schema`

6. Validate with project check:
```sh
git diff --stat
git diff
./project-check.sh
# or: make check / pytest - exact repo check script
# check: exit 0, no failures
```

7. Commit on `task/adapter`:
```sh
git status --short
git add <adapter-file>
git status --short
# check: draft notes file NOT staged/deleted
git commit -m "Finish encode_record: normalize name, add enabled and schema"
git log --oneline -3
git status --short
```

8. Leave ready for review, same checkout:
```sh
pwd
git branch --show-current
# expected: task/adapter in case03/checkouts/adapter-current
git status --short
# do not: push, merge, integrate, publish
```

